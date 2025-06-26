#!/usr/bin/env python3
"""
Tennis Court Reservation Automation
-----------------------------------
Automates the process of booking tennis courts based on YAML configuration.
Accepts optional command-line arguments to override default configuration.
"""

import argparse
import logging
from datetime import date
import traceback
from manager import ReservationManager


def book_court(manager, reservation):
    """Book a court using the provided reservation object"""
    print(f"Booking {reservation.name}:")
    print(f"  Time: {reservation.raw_timeslot}")
    print(f"  Court: {reservation.court}")
    print(f"  User: {reservation.username}")
    print(f"  Days in advance: {reservation.days_in_advance}")

    result = manager.book_reservation(reservation)
    print(f"  Result: {'Success' if result else 'Failed'}\n")
    return result


def main():
    """Main entry point for the reservation system"""
    parser = argparse.ArgumentParser(description='Tennis Court Reservation System')
    parser.add_argument('--config', '-c',
                        help='Path to configuration file (default: auto-detect)')
    parser.add_argument('--timeslot', required=True,
                        help='Timeslot to book (e.g. 17:00)')
    parser.add_argument('--days-advance', dest='days_advance', required=True,
                        help='Days in advance to book (e.g. 7)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')
    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("reservations.log"),
            logging.StreamHandler()
        ]
    )

    # Print date banner
    print(f"=== Tennis Court Reservation: {date.today()} ===\n")

    # Initialize the reservation manager
    try:
        manager = ReservationManager(args.config)
    except Exception as e:
        logging.error(f"Failed to initialize reservation manager: {str(e)}")
        return

    # Process the reservations
    results = {}
    for reservation in manager.reservations:
        reservation.raw_timeslot = args.timeslot

        sport_type = manager.config['settings']['sport_type']
        reservation.timeslot = str(manager.config['time_slots'][sport_type].get(args.timeslot, "1"))

        logging.info(f"Overriding days in advance for {reservation.name}: {args.days_advance}")
        reservation.days_in_advance = args.days_advance

        try:
            results[reservation.name] = book_court(manager, reservation)
        except Exception as e:
            logging.error(f"Error booking {reservation.name}: {str(e)}", exc_info=args.verbose)
            results[reservation.name] = False

    # Print summary
    print("\n=== Booking Summary ===")
    for name, success in results.items():
        print(f"{name}: {'Success' if success else 'Failed'}")

if __name__ == "__main__":
    main()