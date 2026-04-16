import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random

# ========================================================
# HEALTH MEMBERSHIP ANALYTICS TOOL
# Portfolio Project by Richard
# ========================================================

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Member(Person):
    id_count = 1001

    def __init__(self, name, age, membership_type, weight=None, height=None, resting_hr=None):
        super().__init__(name, age)
        self.member_id = Member.id_count
        Member.id_count += 1
        self.membership_type = membership_type
        self.weight = weight
        self.height = height
        self.resting_hr = resting_hr
        self.start_date = datetime.now()
        self.expiry_date = self._calculate_expiry()

    def _calculate_expiry(self):
        days = {"Monthly": 30, "6-Month": 180, "Yearly": 365}
        return self.start_date + timedelta(days=days.get(self.membership_type, 30))

    def __str__(self):
        return (f"ID: {self.member_id} | {self.name} | "
                f"Expires: {self.expiry_date.strftime('%d/%m/%Y')} | "
                f"Membership: {self.membership_type}")


class HealthClubManager:
    def __init__(self, club_name):
        self.club_name = club_name
        self.members = []
        self.membership_prices = {"Monthly": 30, "6-Month": 150, "Yearly": 250}

    def add_member(self, member):
        self.members.append(member)
        print(f"✅ {member.name} added successfully!")

    def show_members(self):
        if not self.members:
            print("\nNo members yet.")
        else:
            print(f"\n--- Member List - {self.club_name} ---")
            for member in self.members:
                print(member)

    def analyze_health(self):
        if not self.members:
            print("No data available for analysis.")
            return

        df = pd.DataFrame([vars(m) for m in self.members])

        # Data Cleaning
        df['weight'] = df['weight'].fillna(df['weight'].mean())
        df['height'] = df['height'].fillna(df['height'].mean())
        df['resting_hr'] = df['resting_hr'].fillna(df['resting_hr'].mean())

        df['BMI'] = df['weight'] / (df['height'] ** 2)

        def bmi_category(bmi):
            if bmi < 18.5: return "Underweight"
            elif 18.5 <= bmi < 25: return "Normal"
            elif 25 <= bmi < 30: return "Overweight"
            return "Obese"

        df['BMI_Category'] = df['BMI'].apply(bmi_category)

        print(f"\n--- HEALTH ANALYTICS REPORT: {self.club_name} ---")
        print(df[['name', 'age', 'BMI', 'BMI_Category', 'resting_hr']])
        print(f"\nAverage BMI: {df['BMI'].mean():.2f}")
        print(f"Average Resting Heart Rate: {df['resting_hr'].mean():.1f} bpm")

        riskiest = df.loc[df['resting_hr'].idxmax()]
        print(f"\n⚠️ Highest risk member: {riskiest['name']} ({riskiest['resting_hr']} bpm)")

    def generate_visual_dashboard(self):
        if not self.members:
            print("❌ No data to generate charts.")
            return

        df = pd.DataFrame([vars(m) for m in self.members])

        # FIX: Full cleaning + BMI calculation inside dashboard
        df['weight'] = df['weight'].fillna(df['weight'].mean())
        df['height'] = df['height'].fillna(df['height'].mean())
        df['resting_hr'] = df['resting_hr'].fillna(df['resting_hr'].mean())
        df['BMI'] = df['weight'] / (df['height'] ** 2)

        def bmi_category(bmi):
            if bmi < 18.5: return "Underweight"
            elif 18.5 <= bmi < 25: return "Normal"
            elif 25 <= bmi < 30: return "Overweight"
            return "Obese"

        df['BMI_Category'] = df['BMI'].apply(bmi_category)

        # Visualizations
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(8, 12))
        plt.style.use('fivethirtyeight')

        status_counts = df['BMI_Category'].value_counts()
        ax1.bar(status_counts.index, status_counts.values, color='#444444')
        ax1.set_title('BMI Status Distribution')
        ax1.set_ylabel('Number of Members')

        ax2.hist(df['age'], bins=10, edgecolor='black')
        ax2.set_title('Age Distribution of Members')
        ax2.set_xlabel('Age')

        ax3.scatter(df['weight'], df['resting_hr'], s=100, alpha=0.6, c='#fc4f30', edgecolor='black')
        ax3.set_title('Weight vs Resting Heart Rate')
        ax3.set_xlabel('Weight (kg)')
        ax3.set_ylabel('Resting Heart Rate (bpm)')

        plt.tight_layout()
        plt.show()
        print("✅ Visual dashboard generated!")

    def export_to_csv(self):
        if self.members:
            df = pd.DataFrame([vars(m) for m in self.members])
            df.to_csv("health_membership_data.csv", index=False)
            print("✅ Data exported to 'health_membership_data.csv'")


# Stress Test
def run_stress_test(manager):
    first_names = ["Arben", "Blerta", "Clirim", "Dafina", "Edon", "Fjolla", "Genci", "Hana", "Ilir", "Jeta"]
    last_names = ["Hoxha", "Leka", "Rama", "Gashi", "Krasniqi", "Mejdani"]
    membership_types = ["Monthly", "6-Month", "Yearly"]

    print("\n🚀 Running Stress Test - Generating 20 members...")

    for _ in range(20):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(18, 65)
        membership_type = random.choice(membership_types)

        weight = random.uniform(60, 110) if random.random() > 0.2 else None
        height = random.uniform(1.60, 1.95) if random.random() > 0.2 else None
        resting_hr = random.randint(55, 110) if random.random() > 0.1 else None

        new_member = Member(name, age, membership_type, weight, height, resting_hr)
        manager.add_member(new_member)

    print("✅ Stress test completed!")


# Main Program
if __name__ == "__main__":
    club = HealthClubManager("TCT Health & Fitness")

    while True:
        print(f"\n--- {club.club_name} MENU ---")
        print("0. Run Stress Test")
        print("1. Show Members")
        print("2. Add New Member")
        print("3. Health Analysis")
        print("4. Export to CSV")
        print("5. Generate Visual Dashboard")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "0":
            run_stress_test(club)
        elif choice == "1":
            club.show_members()
        elif choice == "2":
            try:
                name = input("Name: ")
                age = int(input("Age: "))
                membership_type = input("Membership (Monthly / 6-Month / Yearly): ")
                
                weight_input = input("Weight (kg) - press Enter if unknown: ")
                weight = float(weight_input) if weight_input else None
                
                height_input = input("Height (m) e.g. 1.80: ")
                height = float(height_input) if height_input else None
                
                hr_input = input("Resting Heart Rate (RHR): ")
                resting_hr = int(hr_input) if hr_input else None

                new_member = Member(name, age, membership_type, weight, height, resting_hr)
                club.add_member(new_member)
            except ValueError:
                print("❌ Error in input format!")
        elif choice == "3":
            club.analyze_health()
        elif choice == "4":
            club.export_to_csv()
        elif choice == "5":
            club.generate_visual_dashboard()
        elif choice == "6":
            print("Program closed. Goodbye!")
            break