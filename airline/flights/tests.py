from django.test import Client, TestCase

from .models import Airport, Flights, Passenger

# Create your tests here.


class FlightTestCase(TestCase):

    def setUp(self):

        #create Airports

        a1= Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #create Flights
        Flights.objects.create(origin=a1, destination=a2, duration=100)
        Flights.objects.create(origin=a2, destination=a1, duration=200)
        Flights.objects.create(origin=a1, destination=a2, duration = -100)
        Flights.objects.create(origin=a1, destination=a1, duration=0)

    def test_departures_count(self):
        a= Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)
    
    def test_arrivals_count(self):
        a= Airport.objects.get(code="BBB")
        self.assertEqual(a.arrivals.count(), 2)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f= Flights.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())     