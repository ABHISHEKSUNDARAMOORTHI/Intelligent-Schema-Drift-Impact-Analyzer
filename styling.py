# styling.py
import streamlit as st

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for a professional look."""
    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        /* Import Font Awesome for Icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');


        /* Color Variables for a Brighter, Professional Palette */
        :root {
            --bg-primary: #1a202c; /* Deep Dark Blue-Gray */
            --bg-secondary: #2d3748; /* Slightly Lighter Dark Blue-Gray (Card/Header) */
            --text-light: #e2e8f0; /* Off-White Text */
            --text-medium: #a0aec0; /* Subtler Gray Text */

            --accent-blue-light: #63b3ed; /* Primary Accent Blue */
            --accent-blue-dark: #4299e1; /* Darker Accent Blue */

            --success-color: #4CAF50; /* Bright Green for Additions/Success */
            --danger-color: #EF4444; /* Bright Red for Deletions/Errors */
            --warning-color: #FBBF24; /* Bright Amber for Modifications/Warnings */
            --info-color: #3B82F6; /* Brighter Blue for Info */

            --border-color: #4a5568; /* Subtle Border Color */
            --shadow-light: rgba(0, 0, 0, 0.2);
            --shadow-medium: rgba(0, 0, 0, 0.4);
            --border-radius-lg: 12px;
            --border-radius-md: 8px;
            --border-radius-sm: 4px;
        }

        /* General Body & Typography */
        html, body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-light);
            background-color: var(--bg-primary);
        }

        /* Streamlit App Overrides */
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-light);
        }

        /* Original Header Section (now primarily the main content header) */
        .stApp > header {
            background-color: var(--bg-secondary);
            padding: 1.5rem 2rem;
            box-shadow: 0 4px 8px var(--shadow-medium);
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--border-color);
        }
        /* NOTE: The classes 'header-content h1' and 'header-content p' from previous versions
                 are now superseded by 'hero-title', 'hero-subtitle', 'hero-tagline'
                 for the main entrance. You might want to remove or repurpose them if they
                 are no longer needed for other internal headers. */


        /* --- NEW: Hero Section Styling for a "Bang" Entrance --- */
        .hero-section {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, #1a273b 100%); /* Deep gradient */
            padding: 4rem 2rem; /* More vertical padding */
            text-align: center;
            color: var(--text-light);
            box-shadow: 0 10px 30px var(--shadow-medium); /* Stronger shadow */
            border-bottom: 2px solid var(--accent-blue-dark);
            position: relative; /* For potential background effects */
            overflow: hidden; /* Ensure no overflow from animations */
        }

        /* Subtle pulsating background effect */
        .hero-section::before {
            content: '';
            position: absolute;
            top: -20%;
            left: -20%;
            width: 140%;
            height: 140%;
            background: radial-gradient(circle, rgba(66,153,225,0.1) 0%, transparent 70%);
            animation: pulse-bg 15s infinite alternate ease-in-out;
            z-index: 0;
        }

        @keyframes pulse-bg {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 0.6; }
            100% { transform: scale(1); opacity: 0.8; }
        }

        .hero-title {
            font-size: 3.8rem; /* Massive title */
            color: var(--accent-blue-light);
            margin-bottom: 0.8rem;
            font-weight: 800;
            letter-spacing: -0.06em;
            text-shadow: 0px 4px 10px var(--shadow-medium); /* Very strong shadow */
            position: relative; /* Above pseudo-element */
            z-index: 1;
            animation: slideInFromTop 1s ease-out; /* Animation */
        }
        .hero-title i {
            margin-right: 1rem;
            color: var(--accent-blue-dark); /* Darker icon for contrast */
        }

        .hero-subtitle {
            font-size: 1.8rem; /* Prominent subtitle */
            color: var(--text-medium);
            margin-bottom: 1.5rem;
            font-weight: 400;
            opacity: 0.95;
            line-height: 1.4;
            position: relative;
            z-index: 1;
            animation: fadeIn 1.5s ease-out 0.5s forwards; /* Delayed fade in */
            opacity: 0; /* Start hidden for animation */
        }

        .hero-tagline {
            font-size: 1.4rem;
            color: var(--accent-blue-light);
            font-weight: 600;
            margin-top: 2rem;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
            animation: fadeIn 2s ease-out 1s forwards; /* Further delayed fade in */
            opacity: 0; /* Start hidden for animation */
        }

        @keyframes slideInFromTop {
            0% { transform: translateY(-50px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        /* --- END Hero Section Styling --- */


        /* Main Content Container */
        .main .block-container {
            max-width: 1200px;
            padding: 2.5rem 3rem;
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-lg);
            box-shadow: 0 10px 25px var(--shadow-medium);
            margin: 3rem auto;
            border: 1px solid var(--border-color);
        }

        /* Section Headers */
        .stMarkdown h2 {
            font-size: 2.2rem;
            color: var(--text-light);
            margin-top: 2.5rem;
            margin-bottom: 1.8rem;
            border-bottom: 2px solid var(--accent-blue-light);
            padding-bottom: 0.8rem;
            font-weight: 700;
            position: relative;
        }
        .stMarkdown h2::after {
            content: '';
            display: block;
            width: 70px;
            height: 5px;
            background: linear-gradient(90deg, var(--accent-blue-light), transparent);
            position: absolute;
            bottom: -2px;
            left: 0;
            border-radius: var(--border-radius-sm);
        }

        .stMarkdown h3 {
            font-size: 1.8rem;
            color: var(--accent-blue-light);
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            border-bottom: 1px dashed var(--border-color);
            padding-bottom: 0.6rem;
            font-weight: 600;
        }
        .stMarkdown h4 {
            font-size: 1.4rem;
            color: var(--accent-blue-dark);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }

        /* Textareas and Input Fields */
        textarea, .stTextInput > div > div > input, .stCodeEditor {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            color: var(--text-light);
            font-size: 1.05rem;
            padding: 12px 18px;
            box-shadow: inset 0 2px 5px var(--shadow-light);
            transition: all 0.3s ease;
        }
        textarea:focus, .stTextInput > div > div > input:focus, .stCodeEditor:focus-within {
            border-color: var(--accent-blue-light);
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5), inset 0 2px 5px var(--shadow-light);
            outline: none;
        }
        textarea::placeholder {
            color: var(--text-medium);
            opacity: 0.6;
        }

        /* Buttons */
        .stButton > button {
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--border-radius-md);
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1.8rem;
            box-shadow: 0 8px 15px var(--shadow-medium);
            letter-spacing: 0.03em;
        }
        .stButton > button:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px var(--shadow-medium);
        }
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 4px 8px var(--shadow-light);
        }

        .stButton > button.primary {
            background: linear-gradient(45deg, var(--accent-blue-dark), var(--accent-blue-light));
            color: #ffffff;
            border: 1px solid var(--accent-blue-light);
        }
        .stButton > button.primary:hover {
            background: linear-gradient(45deg, #3182ce, var(--accent-blue-light));
        }

        .stButton > button.secondary {
            background-color: var(--bg-primary);
            color: var(--accent-blue-light);
            border: 2px solid var(--accent-blue-dark);
        }
        .stButton > button.secondary:hover {
            background-color: var(--accent-blue-dark);
            color: #ffffff;
            border-color: var(--accent-blue-dark);
        }
        .stButton > button i {
            margin-right: 0.7rem;
            font-size: 1.2em;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 1.8rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            background-color: transparent;
            color: var(--text-medium);
            border: none;
            padding: 1.2rem 1.8rem;
            font-size: 1.15rem;
            font-weight: 600;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            position: relative;
            overflow: hidden;
        }
        .stTabs [data-baseweb="tab-list"] button:hover:not([aria-selected="true"]) {
            color: var(--text-light);
            background-color: var(--border-color);
            border-radius: var(--border-radius-md) var(--border-radius-md) 0 0;
            transform: translateY(-3px);
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: var(--accent-blue-light) !important;
            border-bottom: 4px solid var(--accent-blue-light) !important;
            background-color: var(--bg-primary) !important;
            transform: translateY(-2px);
        }
        .stTabs [data-baseweb="tab-list"] button i {
            margin-right: 0.8rem;
            font-size: 1.2em;
            color: inherit;
        }

        /* Markdown output styling (for AI explanations) */
        .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
            color: var(--text-light);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        .stMarkdown ul {
            list-style-type: '👉 ';
            margin-left: 30px;
            padding-left: 10px;
        }
        .stMarkdown ol {
            margin-left: 30px;
            padding-left: 10px;
        }
        .stMarkdown strong {
            color: var(--accent-blue-light);
            font-weight: 700;
        }
        .stMarkdown em {
            color: var(--text-medium);
            font-style: italic;
        }
        .stMarkdown code {
            background-color: #4a5568;
            padding: 0.3em 0.5em;
            border-radius: var(--border-radius-sm);
            font-family: 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.95em;
            color: #FFD700;
        }
        .stMarkdown pre code {
            background-color: #0d1217;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1.5em;
            overflow-x: auto;
            margin-bottom: 2rem;
            display: block;
            box-shadow: inset 0 0 10px var(--shadow-light);
            color: #ffffff;
            font-size: 1em;
            line-height: 1.5;
        }

        /* Alerts and Info Boxes */
        .stAlert {
            border-radius: var(--border-radius-md);
            margin-top: 1.5rem;
            padding: 1.2rem 1.8rem;
            font-weight: 600;
            font-size: 1.05rem;
        }
        .stAlert.st-emotion-cache-1fcpknu { /* Success */
            border-left: 8px solid var(--success-color) !important;
            background-color: rgba(76, 175, 80, 0.15) !important;
            color: var(--success-color) !important;
        }
        .stAlert.st-emotion-cache-1wdd6qg { /* Warning */
            border-left: 8px solid var(--warning-color) !important;
            background-color: rgba(251, 191, 36, 0.15) !important;
            color: var(--warning-color) !important;
        }
        .stAlert.st-emotion-cache-1215i5j { /* Error */
            border-left: 8px solid var(--danger-color) !important;
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: var(--danger-color) !important;
        }
        .stInfo { /* Info */
            border-left: 8px solid var(--info-color);
            background-color: rgba(59, 130, 246, 0.15);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            margin-top: 1.5rem;
            color: var(--info-color);
            font-size: 1.1rem;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: var(--border-color);
            color: var(--text-light);
            font-weight: 600;
            border-radius: var(--border-radius-md);
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease;
            box-shadow: 0 3px 8px var(--shadow-light);
            font-size: 1.1rem;
        }
        .streamlit-expanderHeader:hover {
            background-color: #5b6980;
        }
        .streamlit-expanderContent {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
            padding: 1.8rem;
            box-shadow: inset 0 0 10px var(--shadow-light);
        }

        /* Horizontal rule */
        hr {
            border-top: 1px solid var(--border-color);
            margin: 3.5rem 0;
            opacity: 0.6;
        }

        /* --- Custom Metric Card and Grid Styling --- */
        /* Target the Streamlit columns div and make it a grid container */
        div[data-testid="stColumns"]:has(.custom-metric-card) {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
            gap: 1.5rem !important;
            margin-top: 1.5rem !important;
            margin-bottom: 2rem !important;
            padding: 1rem !important;
            background-color: var(--bg-primary) !important;
            border-radius: var(--border-radius-lg) !important;
            box-shadow: inset 0 0 15px var(--shadow-light) !important;
            align-items: stretch !important;
        }
        div[data-testid="stColumns"]:has(.custom-metric-card) > div {
            padding: 0 !important;
            margin: 0 !important;
            min-width: unset !important;
        }


        .custom-metric-card {
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            box-shadow: 0 6px 15px var(--shadow-medium);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 140px;
            border: 1px solid var(--border-color);
            height: 100%;
        }
        .custom-metric-card:hover {
            transform: translateY(-7px);
            box-shadow: 0 10px 25px var(--shadow-medium);
        }

        .custom-metric-content {
            flex-grow: 1;
        }

        .custom-metric-value {
            font-size: 3.2em;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.3rem;
            color: var(--accent-blue-light);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        .custom-metric-label {
            font-size: 1.1em;
            color: var(--text-medium);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.5rem;
        }
        .custom-metric-label i {
            margin-right: 0.8rem;
            color: var(--accent-blue-dark);
        }

        .custom-metric-delta {
            font-size: 1.3em;
            font-weight: 700;
            margin-top: 1rem;
            align-self: flex-end;
            padding: 0.3em 0.7em;
            border-radius: var(--border-radius-sm);
            background-color: rgba(255,255,255,0.08);
        }

        /* Specific card types and their colors */
        .custom-metric-card-info {
            background: linear-gradient(135deg, #2a3447, #1a202c);
            border-left: 6px solid var(--info-color);
            color: var(--text-light);
        }
        .custom-metric-card-info .custom-metric-value {
            color: var(--info-color);
        }

        .custom-metric-card-added {
            background: linear-gradient(135deg, #274029, #1a202c);
            border-left: 6px solid var(--success-color);
            color: var(--text-light);
        }
        .custom-metric-card-added .custom-metric-value {
            color: var(--success-color);
        }
        
        .custom-metric-card-deleted {
            background: linear-gradient(135deg, #4a2d2d, #1a202c);
            border-left: 6px solid var(--danger-color);
            color: var(--text-light);
        }
        .custom-metric-card-deleted .custom-metric-value {
            color: var(--danger-color);
        }

        .custom-metric-card-modified {
            background: linear-gradient(135deg, #473a27, #1a202c);
            border-left: 6px solid var(--warning-color);
            color: var(--text-light);
        }
        .custom-metric-card-modified .custom-metric-value {
            color: var(--warning-color);
        }

        /* Delta colors */
        .custom-metric-delta.delta-positive {
            color: var(--success-color);
        }
        .custom-metric-delta.delta-negative {
            color: var(--danger-color);
        }
        .custom-metric-delta.delta-neutral {
            color: var(--text-medium);
        }


        /* Responsive Design */
        @media (max-width: 1024px) {
            div[data-testid="stColumns"]:has(.custom-metric-card) {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) !important;
                gap: 1rem !important;
            }
            .custom-metric-card {
                min-height: 120px;
                padding: 1.2rem;
            }
            .custom-metric-value {
                font-size: 2.8em;
            }
            .custom-metric-label {
                font-size: 1em;
            }
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding: 1.5rem;
                margin: 1.5rem auto;
                width: 95%;
            }
            .stButton > button {
                display: block;
                width: 100%;
                margin: 0.8rem 0;
            }
            .stMarkdown h1 {
                font-size: 2rem;
            }
            .stMarkdown h2 {
                font-size: 1.7rem;
            }
            .stMarkdown h3 {
                font-size: 1.4rem;
            }
            .stMarkdown h4 {
                font-size: 1.1rem;
            }
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.8rem 1rem;
                font-size: 1rem;
            }
            .stMarkdown ul {
                margin-left: 15px;
            }
            div[data-testid="stColumns"]:has(.custom-metric-card) {
                grid-template-columns: 1fr !important;
                gap: 0.8rem !important;
                padding: 0.8rem !important;
            }
            .custom-metric-card {
                min-height: 100px;
                padding: 1rem;
            }
            .custom-metric-value {
                font-size: 2.5em;
            }
            .custom-metric-label {
                font-size: 0.9em;
            }
        }

        /* --- Interactive Diff Viewer Styling --- */
        .diff-viewer-container {
            background-color: var(--bg-primary); /* Dark background for the diff area */
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1rem;
            margin-top: 1.5rem;
            overflow-x: auto; /* Allow horizontal scrolling for wide tables */
        }

        .diff-table {
            width: 100%;
            border-collapse: collapse; /* Ensure cells share borders */
            margin-bottom: 1rem;
            font-family: 'Fira Code', 'Cascadia Code', monospace; /* Monospace for diff content */
            font-size: 0.95em;
        }

        .diff-table th, .diff-table td {
            padding: 0.6rem 1rem;
            border: 1px solid #4a5568; /* Cell borders */
            vertical-align: top; /* Align content to the top */
        }

        .diff-table th {
            background-color: var(--bg-secondary);
            color: var(--text-light);
            text-align: left;
            font-weight: 600;
        }

        .diff-table tbody tr:nth-child(even) {
            background-color: #2a3447; /* Slightly lighter row background */
        }
        .diff-table tbody tr:nth-child(odd) {
            background-color: var(--bg-primary); /* Darker row background */
        }

        /* Diff Cell Coloring */
        .diff-cell {
            color: var(--text-light); /* Default text color */
        }

        /* Added elements (Green) */
        .diff-added {
            background-color: rgba(76, 175, 80, 0.2); /* Light green background */
            color: var(--success-color); /* Green text */
            font-weight: 500;
        }
        .diff-added-label {
            color: var(--success-color);
            font-weight: 600;
        }

        /* Deleted elements (Red) */
        .diff-deleted {
            background-color: rgba(239, 68, 68, 0.2); /* Light red background */
            color: var(--danger-color); /* Red text */
            text-decoration: line-through; /* Strikethrough for deleted items */
            font-weight: 500;
        }
        .diff-deleted-label {
            color: var(--danger-color);
            font-weight: 600;
        }

        /* Modified elements (Yellow/Orange) */
        .diff-modified {
            background-color: rgba(251, 191, 36, 0.15); /* Light amber background */
            color: var(--warning-color); /* Amber text */
            font-weight: 500;
        }
        .diff-modified-label {
            color: var(--warning-color);
            font-weight: 600;
        }

        /* Renamed elements (Purple/Blue-Violet) - Using a distinct color */
        .diff-renamed {
            background-color: rgba(138, 43, 226, 0.15); /* Light purple background */
            color: #8A2BE2; /* Blue-Violet text */
            font-weight: 500;
        }
        .diff-renamed-label {
            color: #8A2BE2;
            font-weight: 600;
        }

        .diff-viewer-container h4 {
            color: var(--accent-blue-light);
            margin-top: 1rem;
            margin-bottom: 0.8rem;
        }
        .diff-viewer-container h5 {
            color: var(--text-light);
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            border-bottom: 1px dashed var(--border-color);
            padding-bottom: 0.3rem;
        }

    </style>
    """, unsafe_allow_html=True)
