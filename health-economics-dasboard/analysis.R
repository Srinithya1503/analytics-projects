# ==============================================================================
# IQVIA ANALYST MINI-PROJECT: HEALTH ECONOMICS & REAL-WORLD DATA SIMULATION
# AUTHOR: Sri Nithya S
# ==============================================================================

# STEP 1: CREATE REPRODUCIBLE RANDOM NUMBERS
# set.seed() locks in the same "random" numbers every time the script runs,
# which matters for reproducibility in clinical/health-economic analysis.
set.seed(42)
 
# STEP 2: SIMULATE 500 PATIENTS IN THE STANDARD OF CARE (SoC) GROUP
soc_id <- 1:500
soc_group <- rep("Standard of Care", 500)
soc_cost <- rnorm(500, mean = 12000, sd = 1500)   # Average cost around $12,000
soc_hospital <- rpois(500, lambda = 3.5)          # Average 3.5 hospitalizations
soc_qaly <- runif(500, min = 0.55, max = 0.75)    # Quality of life score between 0.55 and 0.75
 
# STEP 3: SIMULATE 500 PATIENTS IN THE NEW DRUG X GROUP
drug_id <- 501:1000
drug_group <- rep("Drug X", 500)
drug_cost <- rnorm(500, mean = 22000, sd = 2000)  # Higher cost around $22,000
drug_hospital <- rpois(500, lambda = 1.8)         # Lower hospitalizations (1.8 average)
drug_qaly <- runif(500, min = 0.70, max = 0.90)   # Better quality of life score
 
# STEP 4: COMBINE GROUPS INTO A SINGLE DATASET
all_ids <- c(soc_id, drug_id)
all_groups <- c(soc_group, drug_group)
all_costs <- c(soc_cost, drug_cost)
all_hospitals <- c(soc_hospital, drug_hospital)
all_qalys <- c(soc_qaly, drug_qaly)
 
patient_data <- data.frame(
  PatientID = all_ids,
  Treatment = all_groups,
  AnnualCost = all_costs,
  Hospitalizations = all_hospitals,
  QALY = all_qalys
)
 
# Quick look at the combined dataset structure
print("--- FIRST 6 ROWS OF SIMULATED DATASET ---")
print(head(patient_data))
 
# STEP 5: CALCULATE AVERAGE VALUES FOR VALUE COMMUNICATION
mean_cost_soc <- mean(patient_data$AnnualCost[patient_data$Treatment == "Standard of Care"])
mean_cost_drug <- mean(patient_data$AnnualCost[patient_data$Treatment == "Drug X"])
mean_qaly_soc <- mean(patient_data$QALY[patient_data$Treatment == "Standard of Care"])
mean_qaly_drug <- mean(patient_data$QALY[patient_data$Treatment == "Drug X"])
 
print("--- GROUP AVERAGES ---")
print(paste("Mean Annual Cost (SoC):", round(mean_cost_soc, 2)))
print(paste("Mean Annual Cost (Drug X):", round(mean_cost_drug, 2)))
print(paste("Mean QALY (SoC):", round(mean_qaly_soc, 4)))
print(paste("Mean QALY (Drug X):", round(mean_qaly_drug, 4)))
 
# STEP 6: CALCULATE THE INCREMENTAL COST-EFFECTIVENESS RATIO (ICER)
# ICER = (extra cost of Drug X) / (extra health benefit of Drug X)
# It answers: "How much more do we pay for each additional unit of health gained?"
delta_cost <- mean_cost_drug - mean_cost_soc
delta_qaly <- mean_qaly_drug - mean_qaly_soc
icer_value <- delta_cost / delta_qaly
 
print("--- HEOR METRICS SUMMARY ---")
print(paste("Incremental Cost:", round(delta_cost, 2)))
print(paste("Incremental QALY Gain:", round(delta_qaly, 4)))
print(paste("Calculated ICER per QALY:", round(icer_value, 2)))
 
# STEP 7: RUN STATISTICAL T-TEST FOR CLINICAL OUTCOMES
# Tests whether the difference in average hospitalizations between the two
# groups is statistically significant (unlikely due to random chance alone).
hospital_ttest <- t.test(Hospitalizations ~ Treatment, data = patient_data)
print("--- T-TEST: HOSPITALIZATIONS BY TREATMENT GROUP ---")
print(hospital_ttest)
 
# STEP 8: CREATE A SIMPLE COST-EFFECTIVENESS VISUALIZATION
# Saves a bar chart comparing average annual cost and average QALY by group.
# This gives a quick visual for the README and for stakeholder presentations.
dir.create("output", showWarnings = FALSE)
 
png("output/icer_plot.png", width = 800, height = 600)
cost_means <- c(mean_cost_soc, mean_cost_drug)
names(cost_means) <- c("Standard of Care", "Drug X")
barplot(
  cost_means,
  main = "Average Annual Treatment Cost by Group",
  ylab = "Annual Cost (USD)",
  col = c("steelblue", "darkorange"),
  ylim = c(0, max(cost_means) * 1.2)
)
dev.off()
 
print("Plot saved to output/icer_plot.png")
 
# STEP 9: EXPORT SUMMARY FOR EXCEL BUDGET IMPACT MODEL
# The exported CSV feeds directly into budget_impact_model.xlsx so a
# non-technical stakeholder can explore the numbers without opening R.
write.csv(patient_data, "patient_dataset_output.csv", row.names = FALSE)
print("Project data exported successfully to patient_dataset_output.csv")
 
