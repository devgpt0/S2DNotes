# Project 09: Hotel Booking Backend Simulator

## Estimated Time
5 to 7 hours

## Goal
Build a booking engine module with room inventory and reservation lifecycle.

## Functional Requirements
- Add room inventory by room type.
- Search available rooms by date range.
- Create booking.
- Cancel booking and release inventory.
- Show occupancy report by date.

## Non-Functional Requirements
- Prevent overbooking.
- Booking IDs must be unique.

## Concepts Practiced
- `Map<String, Integer>` room inventory
- `List<BookingRecord>`
- date-range checks and filtering

## HLD
- `RoomInventoryService`
- `BookingService`
- `AvailabilityService`
- `ReportService`

## LLD
- `isAvailable(roomType, checkIn, checkOut): boolean`
- `createBooking(bookingMap, request): BookingRecord|None`
- `cancelBooking(bookingMap, bookingId): boolean`
- `occupancyReport(bookings, date): Map<String, Integer>`
- `findBookingsByCustomer(bookings, customerId): List<BookingRecord>`

## Passing Criteria
- Booking blocks only when inventory unavailable.
- Cancel returns availability.
- Occupancy report matches bookings.

## Implementation Roadmap
1. Build inventory and booking structures.
2. Add availability logic.
3. Add create/cancel booking.
4. Add occupancy report.
