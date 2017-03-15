require 'bigdecimal'

P_Pos_Sick = BigDecimal.new("0.99")
P_Neg_Sick = BigDecimal.new("0.01")
P_Pos_Healthy = BigDecimal.new("0.01")
P_Neg_Healthy = BigDecimal.new("0.99")
# P_Sick = BigDecimal.new("1e-3")
P_Sick = BigDecimal.new("1e-6")
P_Healthy = BigDecimal.new("1.0") - P_Sick

P_Pos = P_Pos_Sick * P_Sick + P_Pos_Healthy * P_Healthy

P_Sick_Pos = P_Pos_Sick * P_Sick / P_Pos

ppb = BigDecimal.new("0.8")

acc = (ppb * (1 - P_Sick)) / (P_Sick - 2 * P_Sick * ppb + ppb)
