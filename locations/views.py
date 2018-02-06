from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import connection
from .models import Location, Result
from .serializers import LocationSerializer, ResultSerializer

# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    model = Location
    serializer_class = LocationSerializer

    # allows for querying by name of a location
    def get_queryset(self):
        queryset = Location.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class ResultViewSet(viewsets.ViewSet):
    serializer_class = ResultSerializer

    def list(self, request):
        latitude = request.GET.get('latitude', None)
        longitude = request.GET.get('longitude', None)
        radius = request.GET.get('radius', None)
        category = request.GET.get('category', None)
        max_count = request.GET.get('max_count', None)
        if latitude == None or longitude == None or radius == None or max_count == None:
            return Response({'Bad request': 'Not enough parameters, refer to the readme on how to create a proper request.'
                             }, status=status.HTTP_400_BAD_REQUEST)
        # floats can stay as unicode but integers need to be casted as such before running sql query
        max_count = int(max_count)
        # convert radius from meters to kilometers which is needed for sql query
        radius = float(radius) / 1000
        location_results = self.get_locations_in_radius(longitude, latitude, radius, max_count, category)
        serializer = ResultSerializer(
            instance=location_results, many=True)
        if serializer.data == []:
            return Response({'Oops: Looks like there are no locations matching your query. Try changing your parameters.'
                             }, status=status.HTTP_200_OK)
        return Response(serializer.data)

    def get_locations_in_radius(self, longitude, latitude, radius, max_count, category=None):
        with connection.cursor() as cursor:
            # creating two different queries so I dont have to use string interpolation which would put the database at risk for SQL injection
            if category:
                cursor.execute("""
                    SELECT name, st_distance_sphere(POINT(longitude, latitude), POINT(%s, %s)) AS Distance, category
                    FROM locations_location
                    WHERE MBRContains (
                        LineString (
                            Point (
                                longitude + %s / ( 111.1 / COS(RADIANS(latitude))),
                                latitude + %s / 111.1
                            ),
                            Point (
                                longitude - %s / ( 111.1 / COS(RADIANS(latitude))),
                                latitude - %s / 111.1
                            )
                        ),
                        Point (%s, %s)
                    )
                    AND category = %s
                    Order by Distance
                    LIMIT %s;
                """, [longitude, latitude, radius, radius, radius, radius, longitude, latitude, category, max_count])
            else:
                cursor.execute("""
                    SELECT name, st_distance_sphere(POINT(longitude, latitude), POINT(%s, %s)) AS Distance, category
                    FROM locations_location
                    WHERE MBRContains (
                        LineString (
                            Point (
                                longitude + %s / ( 111.1 / COS(RADIANS(latitude))),
                                latitude + %s / 111.1
                            ),
                            Point (
                                longitude - %s / ( 111.1 / COS(RADIANS(latitude))),
                                latitude - %s / 111.1
                            )
                        ),
                        Point (%s, %s)
                    )
                    Order by Distance
                    LIMIT %s;
                """, [longitude, latitude, radius, radius, radius, radius, longitude, latitude, max_count])
            results = cursor.fetchall()
            # creates a list of Result objects from the resulting locations from the database
            return [Result(r[0], r[1], r[2]) for r in results]