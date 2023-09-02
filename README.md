# CLI Accounting System

The CLI Accounting System is a command-line interface application that allows users to manage their accounts, perform financial transactions, and export transaction data to a CSV file. It provides a simple and secure way to handle accounting tasks from the command line.

## Features

- **User Sign Up**: New users can sign up with a unique username and password.

- **User Login**: Registered users can log in using their credentials.

- **Password Change**: Users can change their passwords for added security.

- **Account Management**: Users can deposit money, withdraw funds, view deposit history, and view withdrawal history.

- **Data Export**: Users can export their transaction data to a CSV file.

- **Currency Conversion**: Users can perform currency conversion with up-to-date exchange rates.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/ishanoshada/PyChallenge-Accounting
   ```

2. Navigate to the project directory:

   ```
   cd PyChallenge-Accounting
   ```

3. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - Windows:

     ```
     venv\Scripts\activate
     ```

   - macOS and Linux:

     ```
     source venv/bin/activate
     ```

5. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```
   python app.py
   ```

2. Follow the on-screen instructions to sign up or log in.

3. Use the menu options to manage your account, perform transactions, export data, or convert currency.

## Currency Conversion

To use the currency conversion feature, you need to provide the source currency (e.g., USD), target currency (e.g., EUR), and the amount you want to convert. The application will fetch up-to-date exchange rates and provide the converted amount.

## Data Export

You can export your transaction data to a CSV file by selecting the "Export Data" option from the main menu. The exported CSV file will contain information about your deposits and withdrawals, including timestamps and amounts.

## Authors

- [Ishan oshada](https://github.com/ishanoshada)
- 

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
