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
    parser.add_argument('--courts', '-t', nargs='+', default=['COURT1', 'COURT2', 'COURT3'],
                        help='Specific courts to book (default: COURT1 COURT2 COURT3)')
    parser.add_argument('--username',
                        help='Override username for booking')
    parser.add_argument('--court',
                        help='Override court number for booking')
    parser.add_argument('--timeslot',
                        help='Override timeslot for booking (e.g. 17:30)')
    parser.add_argument('--days-advance',
                        dest='days_advance',
                        help='Override days in advance for booking')
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

    # Check if we have override values from command line
    have_overrides = any([args.username, args.court, args.timeslot, args.days_advance])

    # Process the reservations
    if have_overrides:
        # If we have overrides, use them to create a temporary reservation
        for reservation in manager.reservations:
            if reservation.name == args.courts[0]:  # Use the first specified court as template
                # Create a new reservation with overrides
                if args.username:
                    logging.info(f"Overriding username: {args.username}")
                    reservation.username = args.username
                if args.court:
                    logging.info(f"Overriding court: {args.court}")
                    reservation.court = args.court
                if args.timeslot:
                    logging.info(f"Overriding timeslot: {args.timeslot}")
                    reservation.raw_timeslot = args.timeslot
                    # Update the numeric timeslot value from the configuration
                    sport_type = manager.config['settings']['sport_type']
                    reservation.timeslot = str(manager.config['time_slots'][sport_type].get(args.timeslot, "1"))
                if args.days_advance:
                    logging.info(f"Overriding days in advance: {args.days_advance}")
                    reservation.days_in_advance = args.days_advance

                # Book this single reservation with overrides
                success = book_court(manager, reservation)
                print(f"Booking with overrides: {'Success' if success else 'Failed'}")
                return
    else:
        # Book each requested court using default config
        results = {}
        for court_name in args.courts:
            for reservation in manager.reservations:
                if reservation.name == court_name:
                    try:
                        results[court_name] = book_court(manager, reservation)
                    except Exception as e:
                        logging.error(f"Error booking {court_name}: {str(e)}", exc_info=args.verbose)
                        results[court_name] = False

        # Print summary
        print("\n=== Booking Summary ===")
        for name, success in results.items():
            print(f"{name}: {'Success' if success else 'Failed'}")


if __name__ == "__main__":
    main()