import matplotlib.pyplot as plt
import numpy as np

def main():
    # Data: Annual interest rates (%) per plan
    plans = {
        "Standard": 1.25,
        "Plus": 1.25,
        "Premium": 1.51,
        "Metal": 2.02,
        "Ultra": 2.27
    }

    # Monthly subscription prices (€) per plan
    prices = {
        "Standard": 0,
        "Plus": 3.99,
        "Premium": 8.99,
        "Metal": 15.99,
        "Ultra": 55
    }

    # Ask the user for the amount to be remunerated
    while True:
        try:
            amount_saved = float(input("Enter the amount to remunerate (€): "))
            if amount_saved < 0:
                print("Please enter a positive value.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Calculate monthly interest and net benefit per plan
    monthly_interests = {
        plan: (amount_saved * (interest / 100)) / 12
        for plan, interest in plans.items()
    }

    net_benefits = {
        plan: monthly_interests[plan] - prices[plan]
        for plan in plans
    }

    # Plot 1: Bar chart comparing monthly interest and net benefit
    labels = list(plans.keys())
    x = np.arange(len(labels))
    width = 0.35

    fig1, ax1 = plt.subplots(figsize=(10,6))
    rects1 = ax1.bar(x - width/2, monthly_interests.values(), width, label="Monthly Interest (€)")
    rects2 = ax1.bar(x + width/2, net_benefits.values(), width, label="Net Benefit (€)")

    ax1.set_ylabel("€ per month")
    ax1.set_title(f"Revolut Plans with {amount_saved} € remunerated")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()

    # Add value labels on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f"{height:.2f}",
                        xy=(rect.get_x() + rect.get_width()/2, height),
                        xytext=(0,3), textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.show()

    # Plot 2: Break-even point (minimum amount needed to cover subscription cost)
    break_even = {}
    for plan in plans:
        annual_interest = plans[plan]
        subscription_price = prices[plan]
        if annual_interest > 0:
            break_even[plan] = (subscription_price * 12) / (annual_interest / 100)
        else:
            break_even[plan] = np.nan

    fig2, ax2 = plt.subplots(figsize=(10,6))
    bars = ax2.bar(break_even.keys(), break_even.values(), color='teal')

    ax2.set_ylabel("€ needed to cover subscription")
    ax2.set_title("Minimum remunerated amount to cover plan cost (Break-even)")
    ax2.set_ylim(0, max(break_even.values()) * 1.1)

    # Add labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f"{height:.0f} €",
                     xy=(bar.get_x() + bar.get_width()/2, height),
                     xytext=(0,3),
                     textcoords="offset points",
                     ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # Plot 3: Net benefit evolution for ALL plans
    amounts = np.arange(1000, 100001, 1000)
    net_benefits_per_plan = {plan: [] for plan in plans}

    for c in amounts:
        for plan in plans:
            interest = plans[plan]
            price = prices[plan]
            net_benefit = (c * (interest / 100)) / 12 - price
            net_benefits_per_plan[plan].append(net_benefit)

    # Find break-even point where Metal surpasses Standard
    precise_amounts = np.arange(1000, 100001, 1)
    net_std_precise = (precise_amounts * (plans["Standard"] / 100)) / 12 - prices["Standard"]
    net_metal_precise = (precise_amounts * (plans["Metal"] / 100)) / 12 - prices["Metal"]

    crossover_indices = np.where(net_metal_precise > net_std_precise)[0]
    if len(crossover_indices) > 0:
        crossover_amount = precise_amounts[crossover_indices[0]]
        print(f"\nBreak-even point Metal vs Standard: From {crossover_amount:.2f} € remunerated, Metal is better.")
    else:
        crossover_amount = None
        print("\nMetal does not surpass Standard in the analyzed range.")

    fig3, ax3 = plt.subplots(figsize=(12,7))

    for plan, benefits in net_benefits_per_plan.items():
        ax3.plot(amounts, benefits, label=plan)

    ax3.axhline(0, color="black", linestyle="--", linewidth=0.8)

    if crossover_amount:
        ax3.axvline(crossover_amount, color="red", linestyle="--", linewidth=1.5,
                    label=f"Crossover Metal/Standard ({crossover_amount:.0f} €)")
        ax3.annotate(f"Crossover Metal vs Standard\n{crossover_amount:.0f} €",
                     xy=(crossover_amount, 0),
                     xytext=(crossover_amount + 3000, 20),
                     arrowprops=dict(facecolor='red', arrowstyle='->'),
                     fontsize=10, color='red')

    ax3.set_title("Monthly net benefit (€) evolution by remunerated amount (All Plans)")
    ax3.set_xlabel("Remunerated amount (€)")
    ax3.set_ylabel("Monthly net benefit (€)")
    ax3.legend()
    ax3.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
