# ================================
# Tutorial 6 : Hypothesis Testing
# ================================

# ------------------------------------------------
# Basic imports
# ------------------------------------------------
import numpy as np
from scipy import stats

print("Roll No: 16010124116")
print("Name: Akhil Tyagi")

# =================================================
# Q1. Large Sample Z-Test
# =================================================

# Population variance is known, hence Z-test is applied

# Given data
n = 200
x_bar = 6.5
mu_0 = 7
sigma_sq = 8.5
sigma = np.sqrt(sigma_sq)
alpha = 0.05

print("\nQuestion 1: Test if sample is from the given population")
print("H₀: μ = 7 cm")
print("H₁: μ ≠ 7 cm")

# Test statistic
z_stat = (x_bar - mu_0) / (sigma / np.sqrt(n))
print(f"Sample mean: {x_bar} cm")
print(f"Z-statistic: {z_stat:.3f}")

# Critical value
z_critical = stats.norm.ppf(1 - alpha/2)
print(f"Critical value: ±{z_critical:.3f}")

# Decision
if abs(z_stat) > z_critical:
    print("Decision: Reject H₀")
    print("Conclusion: Sample is not from the given population.")
else:
    print("Decision: Fail to reject H₀")
    print("Conclusion: Sample may be from the given population.")

# ------------------------------------------------
# Q2. One Sample t-Test
# ------------------------------------------------

weights = np.array([150, 152, 149, 151, 148, 152, 150, 151, 153])
n = len(weights)
mu_0 = 151

print("\nQuestion 2: Test if average apple weight is 151 grams")
print("H₀: μ = 151 grams")
print("H₁: μ ≠ 151 grams")

x_bar = np.mean(weights)
s = np.std(weights, ddof=1)
se = s / np.sqrt(n)

t_stat = (x_bar - mu_0) / se
print(f"Sample mean: {x_bar:.2f}")
print(f"t-statistic: {t_stat:.3f}")

df = n - 1
t_critical = stats.t.ppf(1 - alpha/2, df)
print(f"Critical value: ±{t_critical:.3f}")

if abs(t_stat) > t_critical:
    print("Decision: Reject H₀")
    print("Conclusion: Average weight is not 151 grams.")
else:
    print("Decision: Fail to reject H₀")
    print("Conclusion: Average weight can be assumed as 151 grams.")

# ------------------------------------------------
# Q3. Paired t-Test (Before & After Tutoring)
# ------------------------------------------------

scores1 = np.array([85,78,72,90,93,65,79,81,70,75,87,69,82,74,86,88,91,73,77,84])
scores2 = np.array([88,80,75,91,95,68,82,84,73,79,89,71,85,77,90,92,94,76,78,83])
n = len(scores1)

print("\nQuestion 3: Effect of tutoring sessions")
print("H₀: μd = 0")
print("H₁: μd > 0")

d = scores2 - scores1 # Differences are taken as (After − Before)
d_bar = np.mean(d)
s_d = np.std(d, ddof=1)
se_d = s_d / np.sqrt(n)

t_stat = d_bar / se_d
print(f"Mean difference: {d_bar:.2f}")
print(f"t-statistic: {t_stat:.3f}")

df = n - 1
t_critical = stats.t.ppf(1 - alpha, df)
print(f"Critical value: {t_critical:.3f}")

if t_stat > t_critical:
    print("Decision: Reject H₀")
    print("Conclusion: Tutoring had a positive impact.")
else:
    print("Decision: Fail to reject H₀")
    print("Conclusion: No significant improvement observed.")

# ------------------------------------------------
# Q4. Two Sample Z-Test
# ------------------------------------------------

# Large sample sizes, hence Z-test is used

n1, n2 = 1000, 2000
x_bar1, x_bar2 = 25, 23
s1, s2 = 5, 7

print("\nQuestion 4: Test difference between two population means")
print("H₀: μ₁ = μ₂")
print("H₁: μ₁ ≠ μ₂")

se = np.sqrt((s1**2 / n1) + (s2**2 / n2))
z_stat = (x_bar1 - x_bar2) / se

print(f"Z-statistic: {z_stat:.3f}")

z_critical = stats.norm.ppf(1 - alpha/2)
print(f"Critical value: ±{z_critical:.3f}")

if abs(z_stat) > z_critical:
    print("Decision: Reject H₀")
    print("Conclusion: Means differ significantly.")
else:
    print("Decision: Fail to reject H₀")
    print("Conclusion: No significant difference.")

# ------------------------------------------------
# Q5. Two Sample One-Tailed t-Test
# ------------------------------------------------

# Assuming equal population variances (pooled t-test)

athletes = np.array([70,75,78,80,82,85,87,90])
players = np.array([72,74,76,78,79,80,82,83,84,85,87,88])

print("\nQuestion 5: Do basketball players weigh more than athletes?")
print("H₀: μ₁ = μ₂")
print("H₁: μ₂ > μ₁")

x_bar1, x_bar2 = np.mean(athletes), np.mean(players)
s1, s2 = np.std(athletes, ddof=1), np.std(players, ddof=1)
n1, n2 = len(athletes), len(players)

s_p = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
se = s_p * np.sqrt(1/n1 + 1/n2)

t_stat = (x_bar2 - x_bar1) / se
print(f"t-statistic: {t_stat:.3f}")

df = n1 + n2 - 2
t_critical = stats.t.ppf(1 - alpha, df)
print(f"Critical value: {t_critical:.3f}")

if t_stat > t_critical:
    print("Decision: Reject H₀")
    print("Conclusion: Basketball players weigh more on average.")
else:
    print("Decision: Fail to reject H₀")
    print("Conclusion: No sufficient evidence.")