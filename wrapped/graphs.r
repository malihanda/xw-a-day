# imports
library(ggwordcloud)
library(tidyverse)

# histogram of the black squares in each puzzle
black_square_count = read_csv("data/black_squares_each.csv")
ggplot(data = black_square_count, aes(squares)) + 
  geom_histogram(binwidth = 1,
                 col = "#000000",
                 fill = "#941919") +
  xlab("blocks") + ylab("# of puzzles") +
  scale_x_continuous(breaks = c(0, 5, 10, 15, 20, 25)) +
  theme(
    panel.grid = element_line(color = "#cccccc"),
    panel.background = element_rect(fill = "#b3b3b3"),
    plot.background = element_rect(fill = "#b3b3b3",
                                   color = "#b3b3b3"))
ggsave("data/black_square_count.png", height = 3, width = 6)

# histogram of the word length in each puzzle
word_length_count = read_csv("data/entry_lengths.csv")
ggplot(data = word_length_count, aes(len)) + 
  geom_histogram(binwidth = 1,
                 col = "#000000",
                 fill = "#941919") +
  xlab("length") + ylab("# of entries") +
  scale_x_continuous(breaks = c(3, 4, 5, 6, 7)) +
  theme(
    panel.grid = element_line(color = "#cccccc"),
    panel.background = element_rect(fill = "#b3b3b3"),
    plot.background = element_rect(fill = "#b3b3b3",
                                   color = "#b3b3b3"))
ggsave("data/entry_length.png", height = 3, width = 3)

# word cloud of three letter words
entries = read_csv("data/entries.csv")
ggplot(filter(entries, nchar(entry) == 3),
       aes(label = entry, size = n)) +
  geom_text_wordcloud() +
  scale_radius(range = c(0, 20), limits = c(0, NA)) +
  theme_minimal() +
  theme(
    text = element_text(family = "mono"),
    panel.background = element_rect(fill = "#b3b3b3", 
                                    color = "#b3b3b3"),
    plot.background = element_rect(fill = "#b3b3b3",
                                   color = "#b3b3b3"))

ggsave("data/tlw_cloud.png", width = 12, height = 7)

# word cloud of fill
entries = read_csv("data/entries.csv")
ggplot(filter(entries, n > 1), aes(label = entry, size = n)) +
  geom_text_wordcloud() +
  scale_radius(range = c(0, 20), limits = c(0, NA)) +
  theme_minimal() +
  theme(
    text = element_text(family = "mono"),
    panel.background = element_rect(fill = "#b3b3b3", 
                                    color = "#b3b3b3"),
    plot.background = element_rect(fill = "#b3b3b3",
                                   color = "#b3b3b3"))

ggsave("data/fill_cloud.png", width = 15, height = 9)

# bar chart of the letter distributions
letter_dist = read_csv("data/letter_dist.csv")
ggplot(data = letter_dist,
       aes(x = letter, y = prop, fill = type)) + 
  geom_bar(stat = "identity",
           position = position_dodge(width = 0.6)) +
  ylab("proportion") +
  scale_fill_manual(
    labels = c("Wikipedia", "7xwords"),
    values = c("wiki" = "#941919", "xw" = "#610d0d")) +
  theme(
    axis.title.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    legend.title = element_blank(),
    legend.background = element_rect(fill = "#b3b3b3",
                                     color = "#b3b3b3"),
    legend.key = element_rect(fill = "#b3b3b3"),
    panel.grid = element_line(color = "#cccccc"),
    panel.background = element_rect(fill = "#b3b3b3"),
    plot.background = element_rect(fill = "#b3b3b3",
                                   color = "#b3b3b3"))

ggsave("data/letter_dist.png", height = 5.5, width = 10)
