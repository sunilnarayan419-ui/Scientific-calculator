from models import MathRequest, MathResponse, Step, VisualizationData, PlotData
import sympy
from sympy import sympify, latex, solve, diff, integrate, sin, cos, tan, exp, log, Matrix, limit, oo, series, Symbol
import numpy as np
import ast

def generate_plot_data(expr, symbol, start=-10, end=10, points=100) -> Optional[VisualizationData]:
    try:
        # Convert sympy expression to a numerical function
        f = sympy.lambdify(symbol, expr, modules=['numpy'])
        
        x_vals = np.linspace(start, end, points)
        y_vals = f(x_vals)
        
        # Handle potential singularities (infinity) or complex numbers by filtering
        # For simplicity in this demo, we'll just convert to list and let JS handle NaNs if possible,
        # or cleanup here.
        x_list = x_vals.tolist()
        y_list = y_vals.tolist()
        
        return VisualizationData(
            title=f"Graph of ${latex(expr)}$",
            data=[
                PlotData(x=x_list, y=y_list, name=str(expr))
            ]
        )
    except Exception as e:
        # print(f"Plot generation failed: {e}") 
        return None

def solve_math_problem(request: MathRequest) -> MathResponse:
    try:
        # Pre-processing
        expr_str = request.expression.replace("^", "**")
        
        # Matrix Detection (basic)
        is_matrix = expr_str.strip().startswith("[[")
        
        steps = []
        result_latex = ""
        explanation = ""
        vis_data = None
        
        x = Symbol('x')
        
        if is_matrix:
            # Safe eval to get list of lists
            try:
                matrix_data = ast.literal_eval(expr_str)
                mat = Matrix(matrix_data)
                
                if request.mode == "matrix_det" or request.mode == "simplify":
                    result = mat.det()
                    result_latex = latex(result)
                    steps.append(Step(description="Calculated Determinant", latex=f"|A| = {result_latex}"))
                    explanation = "Computed the determinant of the matrix."
                    
                elif request.mode == "matrix_inv":
                    result = mat.inv()
                    result_latex = latex(result)
                    steps.append(Step(description="Calculated Inverse", latex=f"A^{{-1}} = {result_latex}"))
                    explanation = "Computed the inverse matrix."
                    
                elif request.mode == "matrix_eigen":
                    # returns {val: mul, ...}
                    eigenvals = mat.eigenvals()
                    result_latex = latex(eigenvals)
                    steps.append(Step(description="Computed Eigenvalues", latex=f"\\lambda = {result_latex}"))
                    explanation = "Found the eigenvalues."
                else:
                    # Default matrix view
                    result_latex = latex(mat)
                    explanation = "Showing matrix."

            except Exception as e:
                return MathResponse(steps=[], result_latex="\\text{Invalid Matrix}", explanation=str(e))

        else:
            # Symbolic Expression
            expr = sympify(expr_str)

            if request.mode == "simplify":
                result = sympy.simplify(expr)
                result_latex = latex(result)
                steps.append(Step(description="Simplified the expression", latex=result_latex))
                explanation = "Simplified using algebraic rules."
                if result.has(x): vis_data = generate_plot_data(result, x)

            elif request.mode == "solve":
                result = solve(expr, x)
                result_latex = latex(result)
                steps.append(Step(description="Found roots/solutions for x", latex=result_latex))
                explanation = "Solved the equation."
                vis_data = generate_plot_data(expr, x)

            elif request.mode == "derivative":
                result = diff(expr, x)
                result_latex = latex(result)
                steps.append(Step(description="Applied differentiation rules", latex=f"\\frac{{d}}{{dx}} ({latex(expr)})"))
                steps.append(Step(description="Result", latex=result_latex))
                explanation = "Calculated the derivative."
                vis_data = generate_plot_data(result, x)
                
            elif request.mode == "integral":
                result = integrate(expr, x)
                result_latex = latex(result) + " + C"
                steps.append(Step(description="Integrated with respect to x", latex=f"\\int ({latex(expr)}) dx"))
                steps.append(Step(description="Result", latex=latex(result)))
                explanation = "Calculated the indefinite integral."
                vis_data = generate_plot_data(result, x)
                
            elif request.mode == "trigonometry":
                result = sympy.trigsimp(expr)
                result_latex = latex(result)
                steps.append(Step(description="Applied trigonometric identities", latex=result_latex))
                explanation = "Simplified using trigonometric identities."
                vis_data = generate_plot_data(result, x)
                
            elif request.mode == "limit":
                # Default limit x -> 0 for demo, or parse "limit(expr, x, val)"
                # For this simple UI, we assume x -> 0 if not specified
                result = limit(expr, x, 0)
                result_latex = latex(result)
                steps.append(Step(description="Calculated limit as x → 0", latex=f"\\lim_{{x \\to 0}} ({latex(expr)})"))
                steps.append(Step(description="Result", latex=result_latex))
                explanation = "Computed the limit."
                if expr.has(x): vis_data = generate_plot_data(expr, x, -2, 2) # Zoom in near 0

            elif request.mode == "series":
                # Taylor series around x=0, up to x^6
                result = series(expr, x, 0, 6).removeO()
                result_latex = latex(result) + " + O(x^6)"
                steps.append(Step(description="Computed Taylor Series expansion (at x=0)", latex=result_latex))
                explanation = "Approximated the function using a power series."
                vis_data = generate_plot_data(result, x, -2, 2)

            else:
                result_latex = latex(expr)
                explanation = "Showing raw expression."
                if expr.has(x): vis_data = generate_plot_data(expr, x)

        return MathResponse(
            result_latex=result_latex,
            steps=steps,
            explanation=explanation,
            visualization_data=vis_data
        )

    except Exception as e:
        return MathResponse(
            result_latex="\\text{Error}",
            steps=[],
            explanation=f"Could not process: {str(e)}"
        )
