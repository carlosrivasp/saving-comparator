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

# Color scheme selector
st.sidebar.markdown("### 🎨 Color Scheme")
color_scheme = st.sidebar.selectbox(
    "Choose color scheme:",
    options=["Bright", "Dark"],
    index=0
)

# Define color schemes
if color_scheme == "Bright":
    bg_color = 'white'
    text_color = 'black'
    grid_color = 'lightgray'
    bar_colors = ['#1f77b4', '#ff7f0e']  # Blue, Orange
    line_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Blue, Orange, Green, Red, Purple
    teal_color = 'teal'
else:  # Dark
    bg_color = '#2e2e2e'
    text_color = 'white'
    grid_color = '#555555'
    bar_colors = ['#4da6ff', '#ff9933']  # Lighter Blue, Lighter Orange
    line_colors = ['#4da6ff', '#ff9933', '#66ff66', '#ff6666', '#cc99ff']  # Lighter versions
    teal_color = '#40e0d0'

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
amount_saved = st.slider("💰 Enter the amount you want to remunerate (€):", min_value=0, max_value= 100000,step=1000, value=10000)

# Monthly interest and net benefits
monthly_interests = {plan: (amount_saved * (rate / 100)) / 12 for plan, rate in plans_input.items()}
net_benefits = {plan: monthly_interests[plan] - prices_input[plan] for plan in plans_input}

# 📊 Bar chart: Monthly interest vs Net benefit
st.subheader("📊 Monthly Interest vs Net Benefit per Plan")

labels = list(plans_input.keys())
x = np.arange(len(labels))
width = 0.35

fig1, ax1 = plt.subplots(figsize=(10,6))
fig1.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)
rects1 = ax1.bar(x - width/2, monthly_interests.values(), width, label="Monthly Interest (€)", color=bar_colors[0])
rects2 = ax1.bar(x + width/2, net_benefits.values(), width, label="Net Benefit (€)", color=bar_colors[1])

ax1.set_ylabel("€ per month", color=text_color)
ax1.set_title(f"Revolut Plans with {amount_saved:.0f} € remunerated", color=text_color)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, color=text_color)
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.5, color=grid_color)
ax1.tick_params(colors=text_color)
ax1.spines['bottom'].set_color(text_color)
ax1.spines['top'].set_color(text_color)
ax1.spines['right'].set_color(text_color)
ax1.spines['left'].set_color(text_color)

for rect in rects1:
    height = rect.get_height()
    ax1.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom', color=text_color)

for rect in rects2:
    height = rect.get_height()
    ax1.annotate(f"{height:.2f}", xy=(rect.get_x() + rect.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom', color=text_color)

st.pyplot(fig1)

st.markdown("""
### 📋 How to Read This Chart

This chart compares the **monthly interest earned** and the **net benefit** of different Revolut subscription plans based on the amount of money you want to remunerate.

- 🔵 **Blue bars** show the interest you would earn monthly for each plan given the amount you entered.
- 🟠 **Orange bars** show the net benefit after subtracting the monthly subscription cost for each plan.
""")

st.info("""
💡 **Key Insights:**
- Use this visualization to understand which plan offers the **best return** on your money after considering the subscription fee.
- ⚠️ If the net benefit is **negative** (orange bar below zero), it means the plan's subscription fee is higher than the interest earned, so it might not be worth upgrading.
- 🔄 **Adjust the amount** to see how the profitability changes and find the optimal plan for your savings.
""")

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
fig2.patch.set_facecolor(bg_color)
ax2.set_facecolor(bg_color)
bars = ax2.bar(break_even.keys(), break_even.values(), color=teal_color)

ax2.set_ylabel("€ needed to cover subscription", color=text_color)
ax2.set_title("Break-even: Minimum remunerated amount to cover subscription", color=text_color)
ax2.set_ylim(0, max(break_even.values()) * 1.1)
ax2.grid(axis='y', linestyle='--', alpha=0.5, color=grid_color)
ax2.tick_params(colors=text_color)
ax2.spines['bottom'].set_color(text_color)
ax2.spines['top'].set_color(text_color)
ax2.spines['right'].set_color(text_color)
ax2.spines['left'].set_color(text_color)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"{height:.0f} €", xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0,3), textcoords="offset points", ha='center', va='bottom', color=text_color)

st.pyplot(fig2)

st.markdown("""
### 📋 Understanding Break-even Analysis

This chart shows the **minimum amount** you need to remunerate in each plan to cover the monthly subscription cost with the interest earned.

- 🟢 **Teal bars** represent the break-even point (in €) for each plan.
- Higher bars mean you need more money to make the plan profitable.
""")

st.info("""
💡 **Key Insights:**
- If you have **less money** than the break-even amount, the plan will cost you more than it earns.
- If you have **more money** than the break-even amount, the plan becomes profitable.
- 🎯 Compare your current savings with these break-even points to choose the most suitable plan.
- 💰 Plans with lower break-even amounts are more accessible for smaller savings.
""")

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
    fig3.patch.set_facecolor(bg_color)
    ax3.set_facecolor(bg_color)

    for i, (plan, benefits) in enumerate(net_benefits_per_plan.items()):
        color = line_colors[i % len(line_colors)]
        ax3.plot(amounts, benefits, label=plan, color=color, linewidth=2)

    ax3.axhline(0, color=text_color, linestyle="--", linewidth=0.8, alpha=0.7)

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

    ax3.set_title("Monthly Net Benefit (€) Evolution by Remunerated Amount", color=text_color)
    ax3.set_xlabel("Remunerated Amount (€)", color=text_color)
    ax3.set_ylabel("Monthly Net Benefit (€)", color=text_color)
    ax3.legend()
    ax3.grid(True, color=grid_color, alpha=0.5)
    ax3.tick_params(colors=text_color)
    ax3.spines['bottom'].set_color(text_color)
    ax3.spines['top'].set_color(text_color)
    ax3.spines['right'].set_color(text_color)
    ax3.spines['left'].set_color(text_color)

    st.pyplot(fig3)

    st.markdown("""
    ### 📋 Understanding the Evolution Chart
    
    This interactive line chart shows how the **net benefit evolves** as you increase the amount of money you want to remunerate across different plans.
    
    - 📈 **Colored lines** represent each selected plan's net benefit progression.
    - ⚫ **Black dashed line** at zero marks the profitability threshold.
    - 🔴 **Red vertical line** (when visible) shows the crossover point between Standard and Metal plans.
    """)

    st.info("""
    💡 **Key Insights:**
    - Lines **above zero** indicate profitable amounts for that plan.
    - Lines **below zero** mean the subscription costs more than the interest earned.
    - 🎯 **Crossover points** show when upgrading to a higher plan becomes more profitable.
    - 📊 **Steeper lines** indicate plans with higher interest rates that scale better with larger amounts.
    - 🔍 Use the plan selector to compare specific plans and find the optimal switching points.
    """)

else:
    st.warning("Select at least one plan to display the graph.")

# Footer with GitHub link
st.caption("💡 Created by [Carlos Rivas](https://github.com/carlosrivasp) · Powered by Streamlit")
