# ============================================================
# SEM / Path-Coefficient Diagram
# Trust Dimensions -> Intention to Use LLMs -> Continued Engagement
# Built from Table 4.9 (Path Coefficients Assessment, H1-H13)
# Indirect effects from Table 4.10 (H14-H19) are noted as a caption,
# since they are products of existing paths, not separate arrows.
#
# Run in R / RStudio. Requires the "qgraph" package.
# ============================================================

install.packages("qgraph")   # uncomment on first run
library(qgraph)

# ---- 1. Direct path data (Table 4.9) ----------------------
paths <- data.frame(
  hyp = paste0("H", 1:13),
  from = c("Cognitive", "Emotional", "Situational", "Dispositional",
           "HistoryBased", "Institutional",
           "Cognitive", "Emotional", "Situational", "Dispositional",
           "HistoryBased", "Institutional", "Intention"),
  to = c(rep("Intention", 6), rep("Engagement", 6), "Engagement"),
  estimate = c(0.117, 0.220, 0.140, 0.197, 0.139, 0.140,
               0.140, 0.140, 0.117, 0.139, 0.197, 0.220, 0.073),
  pvalue = c(0.026, 0.000, 0.012, 0.000, 0.008, 0.006,
             0.193, 0.002, 0.638, 0.000, 0.000, 0.033, 0.024),
  supported = c("Yes", "Yes", "Yes", "Yes", "Yes", "Yes",
                "No", "Yes", "No", "Yes", "Yes", "Yes", "Yes"),
  stringsAsFactors = FALSE
)

# ---- 2. Nodes -----------------------------------------------
nodes <- c("Cognitive", "Emotional", "Situational", "Dispositional",
           "HistoryBased", "Institutional", "Intention", "Engagement")

node_labels <- c("Cognitive\nTrust", "Emotional\nTrust", "Situational\nTrust",
                 "Dispositional\nTrust", "History-Based\nTrust",
                 "Institutional\nTrust", "Intention to\nUse LLMs",
                 "Continued\nEngagement")

# Manual layout mirrors the original framework: six trust boxes
# stacked on the left, Intention to Use as mediator (bottom-middle),
# Continued Engagement as the outcome (top-right).
layout_matrix <- matrix(c(
  -2,  2.5,   # Cognitive
  -2,  1.5,   # Emotional
  -2,  0.5,   # Situational
  -2, -0.5,   # Dispositional
  -2, -1.5,   # HistoryBased
  -2, -2.5,   # Institutional
  0, -2.0,   # Intention to Use
  2,  1.0    # Continued Engagement
), byrow = TRUE, ncol = 2)

# ---- 3. Build the edge list (predictable row order) ---------
edge_from   <- match(paths$from, nodes)
edge_to     <- match(paths$to,   nodes)
edge_weight <- paths$estimate
edge_label  <- sprintf("%.3f", paths$estimate)
edge_lty    <- ifelse(paths$supported == "Yes", 1, 2)   # solid vs dashed
edge_color  <- ifelse(paths$supported == "Yes", "black", "grey60")

edgelist <- cbind(edge_from, edge_to, edge_weight)

# ---- 4. Draw and save the diagram ----------------------------
out_file <- "SEM_path_diagram.png"   # change path as needed
png(out_file, width = 2600, height = 1900, res = 300)

qgraph(edgelist,
       layout            = layout_matrix,
       labels            = node_labels,
       shape             = "rectangle",
       vsize             = 13, vsize2 = 7,
       label.cex         = 1.05,
       label.scale       = FALSE,
       edge.labels       = edge_label,
       edge.label.cex    = 1.0,
       edge.label.color  = "black",
       edge.color        = edge_color,
       lty               = edge_lty,
       esize             = 6,
       asize             = 6,
       arrows            = TRUE,
       fade              = FALSE,
       color             = c(rep("#BFDFFF", 6), "#FFE8A3", "#C8F2C8"),
       border.color      = "black",
       title             = "SEM Path Diagram: Trust Dimensions -> Intention to Use -> Continued Engagement",
       title.cex         = 1.2,
       mar               = c(6, 5, 5, 5))

legend("bottomleft",
       legend = c("Significant path (p < .05)", "Non-significant path"),
       lty = c(1, 2), col = c("black", "grey60"), lwd = 2,
       bty = "n", cex = 0.85)

mtext(paste(
  "Note: Indirect/mediated effects (Table 4.10) are not drawn as separate arrows, since each",
  "equals the product of an existing pair of paths above. Of H14-H19, only H17 (Dispositional",
  "Trust -> Intention -> Continued Engagement) was significant (Est = 0.029, p = 0.045);",
  "H14, H15, H16, H18, and H19 were not significant.", sep = "\n"),
  side = 1, line = 3.5, cex = 0.65, adj = 0)

dev.off()

cat("Diagram saved to:", normalizePath(out_file), "\n")


# ============================================================
# OPTIONAL ALTERNATIVE: lavaan + semPlot
# ------------------------------------------------------------
# If you prefer the classic lavaan/semPlot look (ellipses, the
# package most associated with "SEM diagrams" in R), you can fix
# every path at its reported estimate and render without fitting
# real data. Uncomment and run the block below instead.
# ============================================================

 install.packages(c("lavaan", "semPlot"))
 library(lavaan)
 library(semPlot)

 model <- '
   Intention   ~ 0.117*Cognitive + 0.220*Emotional + 0.140*Situational +
                 0.197*Dispositional + 0.139*HistoryBased + 0.140*Institutional
   Engagement  ~ 0.140*Cognitive + 0.140*Emotional + 0.117*Situational +
                 0.139*Dispositional + 0.197*HistoryBased + 0.220*Institutional +
                 0.073*Intention
 '

 # lavaan needs *some* data matching the variable names; since every
 # path above is fixed by the modifier (e.g. "0.117*Cognitive"), the
 # values shown will be exactly the fixed coefficients, not estimates
 # from this placeholder data.
 set.seed(1)
 vars <- c("Cognitive", "Emotional", "Situational", "Dispositional",
           "HistoryBased", "Institutional", "Intention", "Engagement")
 dat  <- as.data.frame(matrix(rnorm(200 * length(vars)), 200, length(vars)))
 names(dat) <- vars

 fit <- sem(model, data = dat, do.fit = FALSE)

 semPaths(fit,
          what = "path", whatLabels = "est",
          layout = "tree2", residuals = FALSE,
          sizeMan = 10, edge.label.cex = 1,
          edge.color = "black",
          label.cex = 1.1)