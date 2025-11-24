import os
from agents import ConversationManager
import matplotlib.pyplot as plt
import numpy as np

# Try to import OpenAI (most accessible for students)
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("OpenAI not available - using built-in explanations")

class EnhancedFinancialAdvisor:
    """Optional: LLM-enhanced agent for richer explanations"""
    
    def __init__(self, use_llm=False):
        self.use_llm = use_llm
        self.conversation_manager = ConversationManager()
        
        if use_llm and HAS_OPENAI:
            # Set your OpenAI API key here
            openai.api_key = 'your-key-here'  # Replace with your real key
    
    def get_llm_enhancement(self, calculation_result, user_question):
        """Use LLM to enhance the explanation"""
        if not self.use_llm or not HAS_OPENAI:
            return "🔒 LLM enhancement not available - using built-in explanations"
        
        try:
            prompt = f"""
            Based on this Rule of 72 calculation: {calculation_result}
            For the user question: "{user_question}"
            
            Provide a brief, friendly financial insight (2-3 sentences) that:
            1. Explains what this means practically
            2. Gives one relevant financial tip
            3. Uses simple, encouraging language
            
            Keep it under 100 words.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"⚠️ LLM service temporarily unavailable. {str(e)}"
    
    def create_growth_chart(self, principal=1000, rate=8, years=20):
        """Create a simple investment growth chart"""
        # Calculate doubling periods
        years_to_double = 72 / rate
        doubling_periods = years / years_to_double
        
        # Generate data
        time_points = np.arange(0, years + 1)
        values = principal * (2 ** (time_points / years_to_double))
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, values, 'b-', linewidth=2, label=f'Investment at {rate}%')
        
        # Mark doubling points
        doubling_times = [years_to_double * i for i in range(1, int(doubling_periods) + 1)]
        for t in doubling_times:
            if t <= years:
                value = principal * (2 ** (t / years_to_double))
                plt.plot(t, value, 'ro', markersize=8)
                plt.annotate(f'${value:,.0f}', (t, value), 
                           xytext=(10, 10), textcoords='offset points')
        
        plt.title(f'Investment Growth Visualization\n{rate}% Annual Return (Rule of 72)')
        plt.xlabel('Years')
        plt.ylabel('Investment Value ($)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save chart
        plt.savefig('investment_growth.png')
        plt.close()
        
        return "📈 Chart saved as 'investment_growth.png'"

def main():
    """Main interactive application"""
    print("=" * 60)
    print("💰 RULE OF 72 FINANCIAL ADVISOR SYSTEM")
    print("=" * 60)
    print("\nI can help you understand how long it takes investments to double!")
    print("\nExamples you can try:")
    print("• 'How long to double at 8%?'")
    print("• 'What rate do I need to double in 10 years?'") 
    print("• 'Compare 5%, 8%, and 12% returns'")
    print("• 'Create a growth chart for 7% return'")
    print("• Type 'quit' to exit\n")
    
    advisor = EnhancedFinancialAdvisor(use_llm=False)  # Set to True if you have API key
    conversation_manager = ConversationManager()
    
    while True:
        try:
            user_input = input("\n🎯 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thanks for using the Rule of 72 Advisor! 💰")
                break
            
            if not user_input:
                continue
            
            # Special command for chart
            if 'chart' in user_input.lower() or 'graph' in user_input.lower():
                # Extract rate for chart
                numbers = []
                words = user_input.split()
                for word in words:
                    word = word.replace('%', '')
                    try:
                        num = float(word)
                        if 1 <= num <= 30:
                            numbers.append(num)
                    except ValueError:
                        continue
                
                rate = numbers[0] if numbers else 8
                chart_message = advisor.create_growth_chart(rate=rate)
                print(f"\n{chart_message}")
                continue
            
            # Process normal query
            response = conversation_manager.process_query(user_input)
            print(f"\n{response}")
            
            # Show LLM enhancement if available
            if HAS_OPENAI and len(user_input) < 50:  # Simple queries only
                enhancement = advisor.get_llm_enhancement(
                    conversation_manager.conversation_history[-1], 
                    user_input
                )
                if "not available" not in enhancement:
                    print(f"\n💡 AI Insight: {enhancement}")
            
            # Show conversation history
            if len(conversation_manager.get_conversation_history()) % 3 == 0:
                print(f"\n📝 Conversation history: {len(conversation_manager.get_conversation_history())//2} exchanges")
        
        except KeyboardInterrupt:
            print("\n\nThanks for using the Rule of 72 Advisor! 💰")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try asking your question differently.")

if __name__ == "__main__":
    main()