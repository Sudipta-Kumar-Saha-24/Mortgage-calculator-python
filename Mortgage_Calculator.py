import numpy as np
import matplotlib.pyplot as plt

class Mortgage:
    def __init__(self, loan, years, interest, r_frequency):
        """
        Initializes the Mortgage object with loan details.

        :param loan: Loan amount in AUD.
        :param years: Loan term in years.
        :param interest: Annual interest rate (percentage).
        :param r_frequency: Repayment frequency in days (7, 14, 30).
        """
        self.loan = loan
        self.years = years
        self.interest = interest
        self.r_frequency = r_frequency

    def repayments(self):
        """
        Calculates the repayment amount (P0) using the provided formula.

        :return: Repayment amount in AUD.
        """
        L = self.loan
        Y = self.years
        p = self.interest / 100  # Convert percentage to decimal
        k = self.r_frequency

        # Daily interest factor
        daily_interest_factor = 1 + p / 365

        # Calculate numerator and denominator of the repayment formula
        numerator = L * (daily_interest_factor ** (365 * Y)) * (daily_interest_factor ** k - 1)
        denominator = (daily_interest_factor ** (365 * Y) - 1)

        P0 = numerator / denominator
        return P0

    def balance_after(self, n):
        """
        Calculates the remaining principal balance (Bn) after n years.

        :param n: Number of years.
        :return: Remaining principal balance in AUD after n years.
        """
        if n < 0 or n > self.years:
            raise ValueError("n must be between 0 and the total loan term in years.")

        L = self.loan
        Y = self.years
        p = self.interest / 100  # Convert percentage to decimal
        k = self.r_frequency

        P0 = self.repayments()
        daily_interest_factor = 1 + p / 365

        # Calculate remaining balance using the formula
        Bn = (L * (daily_interest_factor ** (365 * n)) -
              P0 * ((daily_interest_factor ** (365 * n) - 1) / (daily_interest_factor ** k - 1)))

        return Bn

    def __str__(self):
        """
        Returns a user-readable string representation of the Mortgage object.

        :return: String detailing loan amount, term, interest, and repayment.
        """
        repayment_amount = self.repayments()

        # Map repayment frequency in days to descriptive string
        frequency_map = {
            7: "Weekly",
            14: "Fortnightly",
            30: "Monthly"
        }
        frequency_str = frequency_map.get(self.r_frequency, f"{self.r_frequency} days")

        return (f"Loan Amount: {self.loan:.2f} AUD\n"
                f"Loan Term (Years): {self.years}\n"
                f"Interest: {self.interest:.2f}%\n"
                f"{frequency_str} Repayments: {repayment_amount:.2f} AUD")

    def draw_balance_graph(self):
        """
        Plots a graph of the remaining principal balance by year.
        """
        years = np.arange(1, self.years + 1)
        remaining_balances = [self.balance_after(n) for n in years]

        plt.figure(figsize=(10, 6))
        plt.plot(years, remaining_balances, marker='o', linestyle='-', color='b')
        plt.xlabel('Years')
        plt.ylabel('Balance')
        plt.title('Mortgage Balance by Years')
        plt.grid(True)
        plt.xticks(years)  # Ensure all years are marked on x-axis
        plt.tight_layout()
        plt.show()
        
def main():
    """
    Main function to execute the mortgage calculator program.
    """

    # Function to get a positive float input
    def get_positive_float(prompt, input_name):
        while True:
            try:
                value = float(input(prompt))
                if value <= 0:
                    print(f'Value of "{input_name}" should be positive. Try again...')
                else:
                    return value
            except ValueError:
                print("Not a valid float value. Try again...")

    # Function to get a positive integer input
    def get_positive_int(prompt, input_name):
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print(f'Value of "{input_name}" should be positive. Try again...')
                else:
                    return value
            except ValueError:
                print("Not a valid int value. Try again...")

    # Function to get repayment frequency
    def get_repayment_frequency():
        frequency_map = [7, 14, 30]
        while True:
            choice = input("Enter the replayment frequency in days (7, 14 or 30):")

            try:
                choice = int(choice)
                if choice in frequency_map:
                    return choice
                else:
                    print("Value of frequency should be 7, 14 or 30. Try again...")
            except ValueError:
                print("Not a valid int value. Try again...")

    # Collect user inputs with validation
    loan = get_positive_float("Enter Loan Amount in AUD: ", "loan")
    print()
    years = get_positive_int("Enter Loan Term in Years: ", "year")
    print()
    interest = get_positive_float("Enter the Bank's Interest Rate in %: ", "interest")
    print()
    r_frequency = get_repayment_frequency()

    # Create Mortgage object
    mortgage = Mortgage(loan, years, interest, r_frequency)

    # Print Mortgage details
    print("\nProgram's output:")
    print(mortgage)
    print("\n")
    
    choice = input('Would you like to plot the "Balance by Years" graph? (y,n):')
    
    if(choice == 'y'):
        # Plot Remaining Principal Graph
        try:
            mortgage.draw_balance_graph()
        except Exception as e:
            print(f"An error occurred while plotting the graph: {e}")
            
            
if __name__ == "__main__":
    main()
