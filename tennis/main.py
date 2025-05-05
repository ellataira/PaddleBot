#!/usr/bin/env python3
"""
Tennis Court Reservation Automation
-----------------------------------
Automates the process of booking tennis courts based on YAML configuration.
"""

import argparse
import logging
from datetime import date
from manager import ReservationManager


def book_court(manager, court_name):
    """Book a specific court from configuration by name"""
    for reservation in manager.reservations:
        if reservation.name == court_name:
            print(f"Booking {court_name}:")
            print(f"  Time: {reservation.raw_timeslot}")
            print(f"  Court: {reservation.court}")
            print(f"  User: {reservation.username}")
            print(f"  Days in advance: {reservation.days_in_advance}")

            result = manager.book_reservation(reservation)
            print(f"  Result: {'Success' if result else 'Failed'}\n")
            return result

    print(f"{court_name} configuration not found")
    return False


def main():
    """Main entry point for the reservation system"""
    parser = argparse.ArgumentParser(description='Tennis Court Reservation System')
    parser.add_argument('--config', '-c',
                        help='Path to configuration file (default: auto-detect)')
    parser.add_argument('--courts', '-t', nargs='+', default=['COURT1', 'COURT2', 'COURT3'],
                        help='Specific courts to book (default: COURT1 COURT2 COURT3)')
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

    # Book each requested court
    results = {}
    for court in args.courts:
        try:
            results[court] = book_court(manager, court)
        except Exception as e:
            logging.error(f"Error booking {court}: {str(e)}", exc_info=args.verbose)
            results[court] = False

    # Print summary
    print("\n=== Booking Summary ===")
    for court, success in results.items():
        print(f"{court}: {'Success' if success else 'Failed'}")


if __name__ == "__main__":
    main()