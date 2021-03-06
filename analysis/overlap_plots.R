
# get PPI name mapping and expr name mapping
source("ppi_utils.R")
source("expr_utils.R")

plot_pairwise_table <- function(src_table)
{
    # load sql config and get connection
    source("sql_config.R")
    con <- get_sql_conn()

    # load ppi network from db
    data <- dbGetQuery(con, paste("SELECT * FROM ", src_table))

    # prepare data for plotting
    data_table <- table(data[c("ppi", "expr")])
    ppis <- rownames(data_table)
    exprs <- colnames(data_table)
    for (row in 1:nrow(data))
    {
        p <- data[row, "ppi"]
        e <- data[row, "expr"]
        overlap_size <- data[row, "overlap_size"]
        ppi_size <- data[row, "ppi_size"]
        # get PPI coverage (ID coverage by the expression data set in percent)
        ppi_coverage <- overlap_size / ppi_size * 100.0
        # save into the table
        data_table[p,e] <- ppi_coverage
    }

    # prepare for plotting
    library(ggplot2)
    library(reshape2)
    #data_table[1,1] <- -100
    plot_data <- melt(data_table)

    # rename PPIs and Exprs:
    plot_data$ppi = to_short_ppi_name(plot_data$ppi)
    plot_data$expr = to_short_expr_name(plot_data$expr)

    # add size col and row
    ppi_col <- data.frame(ppi=to_short_ppi_name(ppis), expr="", value=-100.0)
    plot_data <- rbind(ppi_col, plot_data)
    expr_row <- data.frame(ppi="", expr=c("", to_short_expr_name(exprs)), value=-100.0)
    plot_data <- rbind(expr_row, plot_data)

    # get ppi sizes
    ppi_sizes <- dbGetQuery(con, paste("SELECT DISTINCT ppi, ppi_size FROM", src_table))
    # get expr sizes
    expr_sizes <- dbGetQuery(con, paste("SELECT DISTINCT expr, expr_size FROM", src_table))


    # generate labels (adding the sizes to the empty rows/cols
    plot_data$label = paste(round(plot_data$value, 1), " %", sep="")
    which_ppi_col = which(plot_data$expr == "" & plot_data$ppi != "")
    plot_data$label[which_ppi_col] = ppi_sizes[,"ppi_size"]
    which_expr_col = which(plot_data$ppi == "" & plot_data$expr != "")
    plot_data$label[which_expr_col] = expr_sizes[,"expr_size"]
    which_corner = which(plot_data$ppi == "" & plot_data$expr == "")
    plot_data$label[which_corner] = "size"

    # plot as heatmap table
    # TODO generalize the heatmap table into a separate function
    p <- ggplot(plot_data, aes(expr, ppi)) +
            geom_tile(aes(fill=value)) +
            scale_fill_gradient2("Percent", low="grey80", mid="red", high="white", limits=c(0,100)) +
            scale_color_gradient2(low="grey40", mid="black", high="black", limits=c(0,100), guide='none') +
            geom_text(aes(label=label, colour=value)) +
            xlab('') + ylab('') +
            theme(# disable grid and axis ticks
                  panel.grid.major=element_blank(),
                  panel.grid.minor=element_blank(),
                  axis.ticks=element_blank(),
                  panel.background=element_blank(),
                  # flip x axis
                  #axis.text.x=element_text(angle=90, hjust=1)
                  axis.text.x=element_text(size=10)
                  )
    return(p)
}

# plot everything as PDF, for vectorized graphics

# plot the ppi and expr overlap (ID overlap)
pdf("../figs/overlap_pairwise_expr_ppi.pdf", width=7, height=3)
p <- plot_pairwise_table("overlap_pairwise_expr_ppi")
p <- p + labs(title="PPI protein coverage by expression data sets")
plot(p)
dev.off()


pdf("../figs/overlap_pairwise_expr_ppi_edges.pdf", width=7, height=3)
p <- plot_pairwise_table("overlap_pairwise_expr_ppi_edges")
p <- p + labs(title="PPI edge coverage by expression data sets")
plot(p)
dev.off()
