import plotly.express as px
import plotly.graph_objects as go
import json
import base64
from io import BytesIO

def create_report_html(scores, feedback, suggestions, responses):
    """
    Create HTML content for the email report.
    
    Args:
        scores: Dictionary of strategy scores and dominant strategy
        feedback: Dictionary of feedback by category
        suggestions: Dictionary of suggestions
        responses: Dictionary of user responses
        
    Returns:
        HTML string content for the email
    """
    # Create HTML content
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Divorce Strategy Profile Results</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #4a90e2;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                padding: 20px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }}
            .section {{
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 1px solid #eee;
            }}
            .score-box {{
                background-color: #f0f5ff;
                border: 1px solid #d0e0ff;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
            }}
            .strategy {{
                font-size: 24px;
                font-weight: bold;
                color: #4a90e2;
            }}
            .category {{
                margin-top: 20px;
                background-color: white;
                border: 1px solid #eee;
                padding: 15px;
                border-radius: 5px;
            }}
            .category h3 {{
                color: #4a90e2;
                margin-top: 0;
            }}
            .suggestions {{
                background-color: #f0fff5;
                border: 1px solid #d0ffe0;
                padding: 15px;
                border-radius: 5px;
                margin-top: 10px;
            }}
            .suggestions ul {{
                padding-left: 20px;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #777;
                font-size: 14px;
            }}
            .chart-container {{
                max-width: 100%;
                height: auto;
                margin: 20px 0;
                text-align: center;
            }}
            .strategy-breakdown {{
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                margin-bottom: 20px;
            }}
            .strategy-item {{
                flex-basis: 22%;
                background-color: #f0f5ff;
                border: 1px solid #d0e0ff;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                margin-bottom: 10px;
            }}
            .strategy-count {{
                font-size: 20px;
                font-weight: bold;
                color: #4a90e2;
            }}
            .matchup {{
                background-color: #fff5f0;
                border: 1px solid #ffe0d0;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .matchup h4 {{
                color: #e24a4a;
                margin-top: 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Your Divorce Strategy Profile Results</h1>
            <p>Thank you for completing the assessment. Here are your personalized results.</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Your Dominant Strategy</h2>
                <div class="score-box">
                    <p>Your dominant divorce strategy is:</p>
                    <p class="strategy">{get_strategy_name(scores['dominant_strategy'])}</p>
                </div>
                <p>{feedback['strategy']}</p>
    """
    
    # Add tie note if applicable
    if scores.get('has_tie', False) and 'tie_note' in feedback:
        html += f"<p><strong>Note:</strong> {feedback['tie_note']}</p>"
    
    html += """
            </div>
            
            <div class="section">
                <h2>Strategy Breakdown</h2>
                <div class="strategy-breakdown">
    """
    
    # Add strategy breakdown
    strategy_names = {
        'G': 'The People‑Pleaser',
        'B': 'The Diplomat',
        'C': 'The Challenger',
        'H': 'The Terminator'
    }
    
    for strategy, count in scores['strategy_counts'].items():
        html += f"""
                    <div class="strategy-item">
                        <p>{strategy_names.get(strategy, strategy)}</p>
                        <p class="strategy-count">{count}</p>
                        <p>questions</p>
                    </div>
        """
    
    html += """
                </div>
                <p>{}</p>
            </div>
            
            <div class="section">
                <h2>General Recommendations</h2>
                <div class="suggestions">
                    <ul>
    """.format(feedback.get('distribution', ''))
    
    # Add general suggestions
    if 'general' in suggestions:
        for suggestion in suggestions['general']:
            html += f"<li>{suggestion}</li>\n"
    
    html += """
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>Strategy Matchups</h2>
                <p>How your strategy interacts with different ex-partner strategies:</p>
    """
    
    # Add matchup advice
    if 'matchups' in suggestions:
        for matchup in suggestions['matchups']:
            html += f"""
                <div class="matchup">
                    <h4>If your ex uses: {matchup['ex_type']}</h4>
                    <p><strong>Risk:</strong> {matchup['risk']}</p>
                    <p><strong>Tip:</strong> {matchup['tip']}</p>
                </div>
            """
    
    # Add overall recommendation
    if 'recommendation' in suggestions:
        html += f"""
                <div class="category" style="margin-top: 20px;">
                    <h3>Overall Recommendation</h3>
                    <p>{suggestions['recommendation']}</p>
                </div>
        """
    
    # Add closing sections
    html += """
            </div>
            
            <div class="section">
                <h2>Next Steps</h2>
                <p>Consider the specific recommendations for your strategy type. Recognize that different approaches work better in different contexts, and flexibility can be valuable.</p>
                <p>If you're encountering persistent conflict, consider bringing in a neutral third party (mediator, collaborative coach) to help create structured communication.</p>
            </div>
            
            <div class="section">
                <h2>Resources</h2>
                <ul>
                    <li><strong>Books:</strong> "Just Separated - A Hands-on Workbook for your Separation & Divorce" (Amazon), "BIFF: Quick Responses to High-Conflict People" by Bill Eddy, "Difficult Conversations" by Douglas Stone</li>
                    <li><strong>Websites:</strong> <a href="https://www.divorceworkshop.ca">www.divorceworkshop.ca</a>, UpToParents.org, OurFamilyWizard.com</li>
                    <li><strong>Apps:</strong> Talking Parents, AppClose, Fayr (co-parenting tools)</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>This assessment is for informational purposes only and does not constitute legal, financial, or psychological advice.</p>
            <p>© 2023 Divorce Strategy Profiler</p>
        </div>
    </body>
    </html>
    """
    
    return html

def get_strategy_name(code):
    """Convert strategy code to name."""
    strategy_names = {
        'G': 'The People‑Pleaser',
        'B': 'The Diplomat',
        'C': 'The Challenger',
        'H': 'The Terminator'
    }
    return strategy_names.get(code, code)
