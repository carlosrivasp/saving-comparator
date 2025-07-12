import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Revolut Comparator", layout="centered")

# Title
st.title("💶 Revolut Account Interest Comparator")

st.write("""
This app allows you to compare **monthly net benefits** for different Revolut remunerated accounts, 
and visualize when it's worth upgrading to a higher plan based on the remunerated amount.
""")

# Default data (can be edited in sidebar)
default_plans = {
    "Standard": 1.25,
    "Plus": 1.25,
    "Premium": 1.51,
    "Metal": 2.02,
    "Ultra": 2.27
}

default_prices = {
    "Standard": 0,
    "Plus": 3.99,
    "Premium": 8.99,
    "Metal": 15.99,
    "Ultra": 55
}

# Sidebar: editable interest rates and subscription prices
st.sidebar.header("Edit Subscription Plans & Interest Rates")

st.sidebar.markdown("### Subscription Prices (€)")
prices_input = {}
for plan in default_prices.keys():
    price_val = st.sidebar.number_input(
        f"{plan} subscription price (€):",
        min_value=0.0, max_value=1000.0, step=0.01,
        value=float(default_prices[plan])
    )
    prices_input[plan] = price_val

st.sidebar.markdown("### Interest Rates (%)")
plans_input = {}
for plan in default_plans.keys():
    rate_val = st.sidebar.number_input(
        f"{plan} interest rate (%):",
        min_value=0.0, max_value=10.0, step=0.01,
        value=float(default_plans[plan])
    )
    plans_input[plan] = rate_val

# User input
amount_saved = st.number_input("💰 Enter the amount you want to remunerate (€):", min_value=0, step=1000, value=10000)

# Monthly interest and net benefits
monthly_interests = {plan: (amount_saved * (rate / 100)) / 12 for plan, rate in plans_input.items()}
net_benefits = {plan: monthly_interests[plan] - prices_input[plan] for plan in plans_input}

# 📊 Bar chart: Monthly interest vs Net benefit
st.subheader("📊 Monthly Interest vs Net Benefit per Plan")

labels = list(plans_input.keys())
x = np.arange(len(labels))
width = 0.35

fig1, ax1 = plt.subplots(figsize=(10,6))
rects1 = ax1.bar(x - width/2, monthly_interests.values(), width, label="Monthly Interest (€)")
rects2 = ax1.bar(x + width/2, net_benefits.values(), width, label="Net Benefit (€)")

ax1.set_ylabel("€ per month")
ax1.set_title(f"Revolut Plans with {amount_saved:.0f} € remunerated")
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects1:
    height = rect.get_height()
    ax1.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom')

for rect in rects2:
    height = rect.get_height()
    ax1.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom')

st.pyplot(fig1)

# 📊 Break-even amounts
st.subheader("📉 Minimum amount to cover plan subscription (Break-even)")

break_even = {}
for plan in plans_input:
    rate = plans_input[plan]
    price = prices_input[plan]
    if rate > 0:
        break_even[plan] = (price * 12) / (rate / 100)
    else:
        break_even[plan] = np.nan

fig2, ax2 = plt.subplots(figsize=(10,6))
bars = ax2.bar(break_even.keys(), break_even.values(), color='teal')

ax2.set_ylabel("€ needed to cover subscription")
ax2.set_title("Break-even: Minimum remunerated amount to cover subscription")
ax2.set_ylim(0, max(break_even.values()) * 1.1)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"{height:.0f} €", xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom')

st.pyplot(fig2)

# 📈 Net benefit evolution with plan selector
st.subheader("📈 Net Benefit Evolution by Remunerated Amount")

# Plan selector
selected_plans = st.multiselect(
    "Select which plans to display:",
    options=list(plans_input.keys()),
    default=list(plans_input.keys())
)

if selected_plans:
    amounts = np.arange(1000, 100001, 1000)
    net_benefits_per_plan = {plan: [] for plan in selected_plans}

    for c in amounts:
        for plan in selected_plans:
            net = (c * (plans_input[plan] / 100)) / 12 - prices_input[plan]
            net_benefits_per_plan[plan].append(net)

    fig3, ax3 = plt.subplots(figsize=(12,7))

    for plan, benefits in net_benefits_per_plan.items():
        ax3.plot(amounts, benefits, label=plan)

    ax3.axhline(0, color="black", linestyle="--", linewidth=0.8)

    # Break-even Metal vs Standard (only if both selected)
    if "Standard" in selected_plans and "Metal" in selected_plans:
        precise_amounts = np.arange(1000, 100001, 1)
        net_std_precise = (precise_amounts * (plans_input["Standard"] / 100)) / 12 - prices_input["Standard"]
        net_metal_precise = (precise_amounts * (plans_input["Metal"] / 100)) / 12 - prices_input["Metal"]

        crossover_indices = np.where(net_metal_precise > net_std_precise)[0]
        if len(crossover_indices) > 0:
            crossover_amount = precise_amounts[crossover_indices[0]]
            ax3.axvline(crossover_amount, color="red", linestyle="--", linewidth=1.5,
                        label=f"Break-even Metal/Standard ({crossover_amount:.0f} €)")
            ax3.annotate(f"{crossover_amount:.0f} €", xy=(crossover_amount, 0),
                         xytext=(crossover_amount + 3000, 20),
                         arrowprops=dict(facecolor='red', arrowstyle='->'),
                         fontsize=10, color='red')

    ax3.set_title("Monthly Net Benefit (€) Evolution by Remunerated Amount")
    ax3.set_xlabel("Remunerated Amount (€)")
    ax3.set_ylabel("Monthly Net Benefit (€)")
    ax3.legend()
    ax3.grid(True)

    st.pyplot(fig3)
else:
    st.warning("Select at least one plan to display the graph.")

# Footer with GitHub link
st.caption("💡 Created by [Carlos Rivas](https://github.com/carlosrivasp) · Powered by Streamlit")
