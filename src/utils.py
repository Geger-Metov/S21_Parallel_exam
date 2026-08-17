from random import choices

def golden_ratio(gender : str, words : list[str]) -> str:
   n = len(words)
   if n == 0:
       return ""
   phi = (1 + 5**0.5) / 2
   probs = []       # список вероятностей
   remaining = 1.0  # оставшаяся сумма вероятности
   for i in range(n - 1):
       p = remaining / phi
       probs.append(p)
       remaining -= p
   probs.append(remaining)  # вероятность последнего слова
   if gender == "М":
       return choices(words, probs, k=1)[0]
   else:
       probs.reverse()
       return choices(words, probs, k=1)[0]
