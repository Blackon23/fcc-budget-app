class Category:
  
  def __init__(self, name):
    self.name = name
    self.ledger = []
  
  def __str__(self):
    title = f"{self.name:*^30}\n"
    items = ""
    total = 0
    #alignment of the output of the category
    for item in self.ledger:
      items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + '\n'
      total += item['amount']
    output = title + items + "Total: " + str(total)
    return output

  #add the deposit of the category to the list ledger
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  #add the withdraw of the category to the list ledger
  def withdraw(self, amount, description=""):
    if(self.check_funds(amount)):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  #current balance of the category based on the deposits and withdrawals
  def get_balance(self):
    total_cash = 0
    for item in self.ledger:
      total_cash += item["amount"]
    return total_cash

  #transfer the amount from one category to another
  def transfer(self, amount, category):
    #check the possibiity of the transfer
    if(self.check_funds(amount)):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    return False

  #check if the amount that is asked is greater than the balance (valid for usage)
  def check_funds(self, amount):
    if(self.get_balance() >= amount):
      return True
    return False

def create_spend_chart(categories):
  spent_amounts = []
  for category in categories:
    #on spent amounts we add the withdrawals
    spent = 0
    for item in category.ledger:
      if item["amount"] < 0:
        spent += abs(item["amount"])
    spent_amounts.append(round(spent, 2))
  #on total we add the total spent amounts of all categories rounded at the second digit
  total = round(sum(spent_amounts), 2)
  #use of the lambda function to calculate the percentage of the spent amounts
  spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))
  header = "Percentage spent by category\n"
  chart = ""
  for value in reversed(range(0, 101, 10)):
    #in value there is the percentage increased by 10 and we align to the right by 3 digits
    chart += str(value).rjust(3) + '|'
    #for every percentage of every category we check if it is greater than the value to set it "o" on the chart
    for percent in spent_percentage:
      if percent >= value:
        chart += " o "
      else:
        chart += "   "
    chart += " \n"
  dashes = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
  descriptions = list(map(lambda category: category.name, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
  #format the categories on columns
  for x in zip(*descriptions):
    dashes += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"
  return (header + chart + dashes).rstrip("\n")
