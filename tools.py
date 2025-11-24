def calculate_rule_72(rate=None, years=None):
    """
    Calculate Rule of 72 - either years to double or required rate
    Formula: T = 72/R or R = 72/T
    """
    if rate is not None and years is not None:
        return {"error": "Please provide either rate OR years, not both"}
    
    if rate is not None:
        if rate <= 0:
            return {"error": "Interest rate must be positive"}
        years_to_double = 72 / rate
        return {
            "rate": rate,
            "years_to_double": round(years_to_double, 2),
            "formula": f"72 / {rate} = {round(years_to_double, 2)} years"
        }
    
    if years is not None:
        if years <= 0:
            return {"error": "Years must be positive"}
        required_rate = 72 / years
        return {
            "years": years,
            "required_rate": round(required_rate, 2),
            "formula": f"72 / {years} = {round(required_rate, 2)}%"
        }
    
    return {"error": "Please provide either rate or years"}

def compare_multiple_rates(rates):
    """
    Compare multiple interest rates using Rule of 72
    """
    comparisons = []
    for rate in rates:
        if rate > 0:
            years = 72 / rate
            comparisons.append({
                "rate": rate,
                "years_to_double": round(years, 2),
                "formula": f"72 / {rate} = {round(years, 2)} years"
            })
    return comparisons
