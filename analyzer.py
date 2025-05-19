import questionnaire

def calculate_scores(responses):
    """
    Calculate scores based on the user's responses.
    Returns a dictionary with strategy counts and the dominant strategy.
    """
    # Initialize strategy counts
    strategy_counts = {
        'G': 0,  # Give-Away
        'B': 0,  # Balanced
        'C': 0,  # Competitive
        'H': 0   # High-Conflict
    }
    
    # Count strategies from responses
    for q_id in range(1, 11):
        question_id = f'question_{q_id}'
        if question_id in responses:
            # Get the chosen option (0-based index)
            try:
                # For single-choice questions, we get the index of the selected option
                sections = questionnaire.get_questionnaire_sections()
                questions = sections[0]['questions']
                
                # Find the matching question
                for question in questions:
                    if question['id'] == question_id:
                        # Get the options and find the index of the selected answer
                        options = question['options']
                        selected_answer = responses[question_id]
                        
                        # Find the index of the selected answer
                        if selected_answer in options:
                            selected_index = options.index(selected_answer)
                            # Get the corresponding strategy value
                            if 'strategy_values' in question and selected_index < len(question['strategy_values']):
                                strategy = question['strategy_values'][selected_index]
                                strategy_counts[strategy] += 1
            except Exception as e:
                print(f"Error processing question {question_id}: {e}")
    
    # Determine dominant strategy
    if sum(strategy_counts.values()) > 0:
        dominant_strategy = max(strategy_counts, key=strategy_counts.get)
    else:
        dominant_strategy = 'B'  # Default to Balanced if no answers
    
    # Check for ties
    top_count = strategy_counts[dominant_strategy]
    ties = [s for s, count in strategy_counts.items() if count == top_count]
    
    # In case of a tie, we'll need to ask the user or use a heuristic
    has_tie = len(ties) > 1
    
    scores = {
        'strategy_counts': strategy_counts,
        'dominant_strategy': dominant_strategy,
        'has_tie': has_tie,
        'tied_strategies': ties if has_tie else [],
        'overall': 0  # We'll calculate this differently
    }
    
    # Get percentage represented by dominant strategy (for overall score)
    total_questions = 10  # Total number of strategy questions
    if total_questions > 0 and top_count > 0:
        scores['overall'] = round((top_count / total_questions) * 100)
    else:
        scores['overall'] = 0
    
    return scores

def generate_feedback(scores, responses):
    """Generate personalized feedback based on dominant strategy."""
    feedback = {}
    
    # Get strategy information from the questionnaire module
    try:
        strategy_info = questionnaire.strategy_information
    except:
        # Fallback if not available
        strategy_info = {
            'G': {
                'label': 'The People‑Pleaser',
                'strength': 'You lower tension and keep dialogue open, which can speed practical resolutions.',
                'watch_out': 'You risk giving up long-term security. Establish non-negotiable must-haves and get professional advice.',
                'description': 'Avoids conflict and gives too much to keep the peace—often at their own expense.'
            },
            'B': {
                'label': 'The Diplomat',
                'strength': 'You protect yourself while staying child-focused. Courts and mediators respect this stance.',
                'watch_out': 'A highly aggressive ex can see cooperation as weakness. Set hard deadlines and document every exchange.',
                'description': 'Firm, fair, and child-focused—seeks balance and practical solutions.'
            },
            'C': {
                'label': 'The Challenger',
                'strength': 'You secure resources and discourage exploitation.',
                'watch_out': 'Winning every point may damage future co-parenting. Offer one visible goodwill concession to reduce resistance.',
                'description': 'Tests limits relentlessly, prioritizing wins over harmony.'
            },
            'H': {
                'label': 'The Terminator',
                'strength': 'You expose hidden issues and show you\'re no pushover.',
                'watch_out': 'Conflict spirals drive costs and stress sky-high. Delegate communication to lawyers and seek mental-health support.',
                'description': 'Relentless and uncompromising—demands total victory, no matter the cost.'
            }
        }
    
    dominant = scores['dominant_strategy']
    
    # Create feedback for the dominant strategy
    if dominant in strategy_info:
        strategy_data = strategy_info[dominant]
        
        feedback['strategy'] = f"""
        Your dominant divorce strategy is: {strategy_data['label']}
        
        {strategy_data['description']}
        
        STRENGTH: {strategy_data['strength']}
        
        WATCH OUT: {strategy_data['watch_out']}
        """
    else:
        feedback['strategy'] = "We couldn't determine your dominant strategy clearly."
    
    # Add feedback for tie scenarios if applicable
    if scores['has_tie']:
        tied_strategies = scores['tied_strategies']
        tied_labels = [strategy_info[s]['label'] for s in tied_strategies if s in strategy_info]
        feedback['tie_note'] = f"""
        Note: Your results show equal tendencies toward multiple strategies: {', '.join(tied_labels)}.
        Consider which description feels most accurate to you.
        """
    
    # Add feedback about strategy distribution
    counts = scores['strategy_counts']
    feedback['distribution'] = f"""
    Your strategy breakdown:
    - The People‑Pleaser: {counts['G']} questions
    - The Diplomat: {counts['B']} questions
    - The Challenger: {counts['C']} questions
    - The Terminator: {counts['H']} questions
    """
    
    # Overall summary
    if dominant == 'G':
        feedback['overall'] = """
        You are far too lenient as a People-Pleaser and your ex may walk all over you in the divorce, 
        potentially resulting in an unfair agreement that disadvantages you significantly. 
        You need to assert your needs and rights more clearly to avoid long-term regret.
        """
    elif dominant == 'B':
        feedback['overall'] = """
        As a Diplomat, it's obvious you're trying to be fair toward your ex, but be cautious—if your ex 
        is neither a People-Pleaser nor a Diplomat, your fairness may not be reciprocated. This could give 
        your ex an advantage while leaving you at a disadvantage in the final agreement.
        """
    elif dominant == 'C':
        feedback['overall'] = """
        As a Challenger, it's OK to strive for the best outcome for each issue in the divorce agreement, 
        but remember that the best outcome is a 'win-win' agreement. This means sometimes you win and 
        sometimes your ex wins—you simply can't win everything without creating lasting resentment.
        """
    elif dominant == 'H':
        feedback['overall'] = """
        Your Terminator approach risks causing extreme anger in your ex that may be used against you. 
        You risk your children becoming angry at you for putting their other parent through a difficult divorce, 
        escalating legal costs significantly, and potentially dragging the divorce out for many years with no resolution.
        """
    
    return feedback

def generate_improvement_suggestions(scores, responses):
    """Generate specific suggestions based on strategy type and matchups."""
    suggestions = {}
    
    dominant = scores['dominant_strategy']
    
    # Get matchup advice from questionnaire
    try:
        matchup_advice = questionnaire.matchup_information
    except:
        # Fallback if not available
        matchup_advice = [
            {
                'your': 'G',
                'ex': ['C', 'H'],
                'risk': 'Being steam-rolled; long-term insecurity.',
                'tip': 'Add clear boundaries and retain a strong lawyer/coach.'
            },
            {
                'your': 'B',
                'ex': ['H'],
                'risk': 'Fair offers seen as weakness; dragged into conflict.',
                'tip': 'Insist on written protocols; document everything.'
            },
            {
                'your': 'C',
                'ex': ['G'],
                'risk': 'Asset win may harm co-parenting or reputation.',
                'tip': 'Consider child-centered compromises; show goodwill.'
            },
            {
                'your': 'C',
                'ex': ['C'],
                'risk': 'Legal arms-race and ballooning costs.',
                'tip': 'Propose capped-fee mediation or arbitration.'
            },
            {
                'your': 'H',
                'ex': ['G','B','C','H'],
                'risk': 'High stress and runaway fees.',
                'tip': 'Shift toward assertive (not punitive) tactics; prioritize therapy.'
            },
            {
                'your': 'G',
                'ex': ['B'],
                'risk': 'Over-giving despite balanced offers.',
                'tip': 'Mirror your ex\'s firmness; ask for equitable splits.'
            },
            {
                'your': 'B',
                'ex': ['C'],
                'risk': 'Gradual concession creep.',
                'tip': 'Define red-lines early; use a mediator to enforce them.'
            }
        ]
    
    # General suggestions based on dominant strategy
    if dominant == 'G':
        suggestions['general'] = [
            "You MUST make a list of non-negotiable must-haves and refuse to compromise on them",
            "Hire a strong divorce attorney who can be assertive for you when you cannot",
            "Get professional financial advice before agreeing to ANY settlement",
            "Never agree to anything in the moment—always say 'I'll discuss this with my advisor'"
        ]
    elif dominant == 'B':
        suggestions['general'] = [
            "Be prepared to match your ex's strategy—if they escalate, you may need to as well",
            "Set clear boundaries and enforce them consistently, especially if your ex is not reciprocating fairness",
            "Document every interaction and draft all agreements with your interests strongly protected",
            "Consider having a 'red line' list of items where you will not compromise regardless of pressure"
        ]
    elif dominant == 'C':
        suggestions['general'] = [
            "Identify which issues truly matter most to you and be willing to concede on others",
            "Make strategic concessions to build goodwill and avoid developing a reputation for unreasonableness",
            "Calculate the long-term relationship costs against the financial gains for each contested item",
            "Use a skilled mediator who can help find win-win solutions for high-conflict issues"
        ]
    elif dominant == 'H':
        suggestions['general'] = [
            "Recognize that 'winning' the divorce often means losing in other ways (relationship with children, stress, time)",
            "Set a strict budget with your lawyer to avoid financial devastation from prolonged legal battles",
            "Work with a therapist specifically on managing your anger and aggressive tendencies during negotiations",
            "Consider the true costs of a high-conflict approach—emotional health, co-parenting ability, and children's wellbeing"
        ]
    
    # Add matchup-specific advice
    suggestions['matchups'] = []
    for advice in matchup_advice:
        if advice['your'] == dominant:
            suggestion = {
                'ex_type': ', '.join([get_strategy_name(ex) for ex in advice['ex']]),
                'risk': advice['risk'],
                'tip': advice['tip']
            }
            suggestions['matchups'].append(suggestion)
    
    # Add overall recommendation
    if dominant in ['G', 'H']:
        suggestions['recommendation'] = "Consider working toward a more balanced approach for better long-term outcomes."
    else:
        suggestions['recommendation'] = "Your current strategy is generally effective. Adjust based on how your ex responds."
    
    return suggestions

def get_strategy_name(code):
    """Convert strategy code to name."""
    strategy_names = {
        'G': 'The People‑Pleaser',
        'B': 'The Diplomat',
        'C': 'The Challenger',
        'H': 'The Terminator'
    }
    return strategy_names.get(code, code)
