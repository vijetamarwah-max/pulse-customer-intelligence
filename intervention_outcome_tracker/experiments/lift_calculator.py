class LiftCalculator:
    def calculate(self, pulse_revenue, control_revenue):
        return round(float(pulse_revenue) - float(control_revenue), 3)
