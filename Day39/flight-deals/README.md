# Refactoring

## main.py

Summary of Refactoring Changes:

1. Type Hinting: Added type hints to all function signatures and key variables (e.g., List[Dict[str, Any]]) for better code analysis and readability.
2. Modular Functions:
    update_iata_codes(): Logic for checking and updating IATA codes is now in its own function.
    check_for_cheap_flights(): The main loop for finding flights and sending notifications is now a dedicated function.
    main(): The main execution block is cleaner, showing the high-level steps of the program.
3. Redundancy Removed:
    Removed duplicate if conditions that were checking the flight price.
    Removed the redundant import statement.
    Consolidated the notification logic.
4. Bug Fix:
    Replaced the erroneous notification_manager.send_whatsapp(...) call with notification_manager.send_sms(...).
    Removed the unnecessary print(notification_manager.send_whatsapp) line.
5. Clarity and Readability:
    Removed instructional comments to make the code look more like a finished application.
    Added main guard (if **name** == "**main**":) which is a standard Python best practice.
    Improved print statements to give clearer feedback as the script runs.
    This refactored code is much cleaner, easier to debug, and more aligned with Python best practices.

## data_manager.py

This version introduces:
Type Hinting: For clearer and safer code.
Error Handling: try...except blocks for network requests to prevent crashes.
Docstrings: To explain the purpose of the class and its methods.
Clarity: Using requests directly and ensuring consistent data types.

## notification_manager.py

This version improves the NotificationManager by adding type hints, robust error handling for missing configuration, and a clear method for sending SMS alerts.

## flight_data.py

This file defines a structured data class for holding flight information, making it easier to pass data between different parts of your application.

## flight_search.py

This version adds type hints, improves error handling, and clarifies the logic for fetching API tokens and searching for flights.
