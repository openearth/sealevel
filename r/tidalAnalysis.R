
require(tidyverse)
require(stringr)

filelist <- list.files("p:/11202493--systeemrap-grevelingen/1_data/Wadden/ddl/calculated/TA_filtersurge", pattern = "csv", full.names = T)

filelistShort <- list.files("p:/11202493--systeemrap-grevelingen/1_data/Wadden/ddl/calculated/TA_filtersurge", pattern = "csv", full.names = F)

# get names of stations and year from filenames in filelistShort
# 

names <- tibble(name = str_replace(filelistShort, pattern = "_UTC\\+1.csv", replacement = "")) %>%
  separate(name, c("station", "jaar", "component"), sep = "_") %>%
  select(-component)

df <- lapply(filelist, function(x) read_csv(x))
dfs <- bind_rows(df)

names %>% 
  mutate(jaar = as.integer(jaar)) %>%
  mutate(data = df) %>%
  unnest(cols = data) %>%
  filter(comp %in% c("M2", "M4")) %>%
  filter(station %in% c("DELFZL", "DENHDR", "EEMSHVN", "HARLGN", "HOLWD", "HUIBGT")) %>% 
  pivot_longer(
    cols = c(A, phi_deg), 
    names_to = "variable", 
    values_to = "value"
  ) %>%
  pivot_wider(
    id_cols = c(station, jaar, variable), 
    names_from = comp, 
    values_from = value
  ) %>%
  mutate(
    M2_M4 = case_when(
    variable == "A" ~ M4 / M2,
    variable == "phi_deg" ~ M4 - M2
    )
  ) %>%
  mutate(wanneer = ifelse(jaar < 1993, "voor", "na")) %>%
  ggplot(aes(x = jaar, y = M2_M4)) +
  geom_line(aes(color = wanneer), size = 1) +
  # geom_boxplot(aes(group = wanneer), fill = "transparent") +
  # geom_vline(xintercept = 1993) +
  coord_cartesian(ylim = c(NA,NA)) +
  facet_grid(variable ~ station, scales = "free_y")

dir.create("results")
dir.create("results/tidal_analysis")
ggsave("results/tidal_analysis/M4_M2_wadden.png", height = 5, width = 10)

# genormaliseerde componenten in de tijd

names %>% 
  mutate(jaar = as.integer(jaar)) %>%
  mutate(data = df) %>%
  unnest(cols = data) %>%
  filter(comp %in% c("M2", "M4")) %>%
  filter(station %in% c("DELFZL", "DENHDR", "EEMSHVN", "HARLGN", "HOLWD", "HUIBGT")) %>% 
  group_by(station, comp) %>%
  mutate(Anorm = A/mean(A)) %>%
  ungroup() %>%
  mutate(wanneer = ifelse(jaar < 1993, "voor", "na")) %>%
  ggplot(aes(x = jaar, y = Anorm)) +
  geom_line(aes(color = station), size = 1) +
  # geom_boxplot(aes(group = wanneer), fill = "transparent") +
  # geom_vline(xintercept = 1993) +
  coord_cartesian(ylim = c(NA,NA)) +
  facet_grid(comp ~ ., scales = "free_y")

