import json
from tools import calculate_rule_72, compare_multiple_rates

class Rule72Calculator:
    """Agent 1: Handles the mathematical calculations"""
    
    def __init__(self):
        self.memory = []
    
    def calculate(self, user_input):
        """Extract numbers and perform Rule of 72 calculation"""
        # simple number extraction from text
        numbers = []
        words = user_input.split()
        for word in words:
            word = word.replace('%', '').replace('years', '').replace('year', '')
            try:
                num = float(word)
                numbers.append(num)
            except ValueError:
                continue
        
        if len(numbers) == 1:
            # assume it's an interest rate
            result = calculate_rule_72(rate=numbers[0])
        elif len(numbers) >= 2:
            # use context to determine what user wants
            if 'year' in user_input.lower() or 'double' in user_input.lower():
                result = calculate_rule_72(years=numbers[0])
            else:
                result = calculate_rule_72(rate=numbers[0])
        else:
            result = {"error": "No numbers found in your question"}
        
        self.memory.append({"input": user_input, "result": result})
        return result

class FinancialEducator:
    """Agent 2: Explains the results in friendly terms"""
    
    def __init__(self):
        self.explanations = []
    
    def explain_calculation(self, calculation_result):
        """Generate friendly explanation of Rule of 72 results"""
        if "error" in calculation_result:
            return calculation_result["error"]
        
        if "years_to_double" in calculation_result:
            rate = calculation_result["rate"]
            years = calculation_result["years_to_double"]
            explanation = f"""
**Rule of 72 Calculation:**

• At {rate}% annual interest, your investment will double in approximately **{years} years**
• Formula: 72 ÷ {rate} = {years} years
• This means every ${1,000} would become ${2,000} in {years} years!

**Pro Tip:** The Rule of 72 works because of compound interest. Your earnings start earning their own earnings!
            """
        else:
            years = calculation_result["years"]
            rate = calculation_result["required_rate"]
            explanation = f"""
**Rule of 72 Calculation:**

• To double your money in {years} years, you need approximately **{rate}%** annual return
• Formula: 72 ÷ {years} = {rate}%
• This helps set realistic investment expectations!

**Pro Tip:** Different investments offer different returns: stocks average 7-10%, bonds 3-5%, savings accounts 1-2%
            """
        
        self.explanations.append(explanation)
        return explanation
    
    def compare_rates(self, rates=[5, 8, 10, 12]):
        """Compare multiple interest rates"""
        comparisons = compare_multiple_rates(rates)
        
        explanation = "**Comparison of Different Interest Rates:**\n\n"
        for comp in comparisons:
            explanation += f"• At {comp['rate']}%: doubles in {comp['years_to_double']} years\n"
        
        explanation += "\n**Key Insight:** Higher returns dramatically reduce the time needed to double your money!"
        return explanation

class ConversationManager:
    """Agent 3: Manages the conversation flow and memory"""
    
    def __init__(self):
        self.calculator = Rule72Calculator()
        self.educator = FinancialEducator()
        self.conversation_history = []
    
    def process_query(self, user_input):
        """Main method to handle user queries"""
        # store user input
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # decide what type of query this is
        if any(word in user_input.lower() for word in ['compare', 'multiple', 'different']):
            # comparison request
            rates = [5, 8, 10, 12]  # default rates
            # get rates from input if given
            numbers = []
            words = user_input.split()
            for word in words:
                word = word.replace('%', '')
                try:
                    num = float(word)
                    if 1 <= num <= 30: # reasonable interest rate range
                        numbers.append(num)
                except ValueError:
                    continue
            
            if numbers:
                rates = numbers
            
            result = self.educator.compare_rates(rates)
        
        else:
            # single calculation request
            calculation = self.calculator.calculate(user_input)
            result = self.educator.explain_calculation(calculation)
        
        # store agent response
        self.conversation_history.append({"role": "assistant", "content": result})
        
        return result
    
    def get_conversation_history(self):
        """Return the conversation history"""
        return self.conversation_history