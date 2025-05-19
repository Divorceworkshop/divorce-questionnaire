def get_questionnaire_sections():
    """Define the questionnaire structure with sections and questions."""
    
    sections = [
        {
            'title': 'Divorce Strategy Profiler',
            'questions': [
                {
                    'id': 'question_1',
                    'text': 'When you receive a first settlement offer, what do you do?',
                    'type': 'single_choice',
                    'options': [
                        'Accept quickly just to move on.',
                        'Ask clarifying questions, then counter with data.',
                        'Counter with a higher (or lower) figure to anchor negotiations.',
                        'Reject immediately—no matter how reasonable—and threaten court.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_2',
                    'text': 'How do you share financial or parenting information during the process?',
                    'type': 'single_choice',
                    'options': [
                        'Hand over every document without being asked.',
                        'Exchange items through an agreed checklist and timeline.',
                        'Provide documents only after receiving equivalent information.',
                        'Delay disclosure to make the other side feel powerless.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_3',
                    'text': 'Which statement best describes your legal‑representation choice?',
                    'type': 'single_choice',
                    'options': [
                        'I rely on my ex\'s lawyer or go without one.',
                        'I propose mediation or collaborative law.',
                        'I hired an assertive litigator for leverage.',
                        'I\'ll switch to an even more aggressive lawyer to show I\'m ready to fight.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_4',
                    'text': 'How do you propose or respond to parenting‑time schedules?',
                    'type': 'single_choice',
                    'options': [
                        'I give my ex most of the time with the children to avoid conflict.',
                        'I suggest a schedule built around the children\'s routines.',
                        'I\'m the better parent, so I should have the children most of the time.',
                        'I use parenting time as a bargaining chip or punishment.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_5',
                    'text': 'What is the usual tone of your emails or texts about divorce issues?',
                    'type': 'single_choice',
                    'options': [
                        'Apologetic and self‑blaming; I avoid conflict.',
                        'Courteous, concise, and factual; I expect the same.',
                        'Formal, firm, and sometimes harsh; I won\'t show weakness.',
                        'Threatening and intimidating; I want my ex to feel scared.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_6',
                    'text': 'How do you react when your ex makes a concession?',
                    'type': 'single_choice',
                    'options': [
                        'Offer an even bigger concession in return.',
                        'Match the concession with something of similar value.',
                        'Bank the concession and push for more next time.',
                        'Treat the concession as weakness and demand even more.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_7',
                    'text': 'Which phrase best captures your financial priority?',
                    'type': 'single_choice',
                    'options': [
                        '"I\'ll be okay—take what you need."',
                        '"Let\'s split things so both of us stay solvent."',
                        '"I earned it; I want my full share."',
                        '"I want every asset I can get—plus extra."'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_8',
                    'text': 'How do you feel about your anger toward your ex, and how will you handle it?',
                    'type': 'single_choice',
                    'options': [
                        '"I\'m mostly to blame; I\'ll swallow my anger and keep the peace."',
                        '"I\'m hurt, but I\'ll manage my anger constructively—therapy, journaling, mediation."',
                        '"My anger is justified; I\'ll channel it into getting the best legal outcome."',
                        '"My ex deserves to be crushed, and I won\'t stop until they pay."'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_9',
                    'text': 'What\'s your pattern around negotiation deadlines?',
                    'type': 'single_choice',
                    'options': [
                        'I rush to respond well before they\'re due.',
                        'I meet deadlines reliably and on time.',
                        'I use the full time to refine my stance.',
                        'I ignore deadlines or move the goalposts so my ex knows I\'m in control.'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                },
                {
                    'id': 'question_10',
                    'text': 'How do you view the post‑divorce relationship?',
                    'type': 'single_choice',
                    'options': [
                        '"I\'d like us to stay friends."',
                        '"Civility matters for co‑parenting."',
                        '"Minimal contact once the business is done."',
                        '"I\'ll do whatever it takes to stay in control of my ex."'
                    ],
                    'strategy_values': ['G', 'B', 'C', 'H']
                }
            ]
        },
        {
            'title': 'Email for Results',
            'questions': [
                {
                    'id': 'email',
                    'text': 'Enter your email address to receive your personalized assessment results:',
                    'type': 'email'
                }
            ]
        }
    ]
    
    # Strategy labels and descriptions for analysis
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
    
    # Matchup advice for different strategy combinations
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
    
    # Make strategy information available to other modules
    global strategy_information
    global matchup_information
    strategy_information = strategy_info
    matchup_information = matchup_advice
    
    return sections
