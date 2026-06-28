#!/usr/bin/env python3
"""
Generate interactive HTML and PDF study materials for AB-100 Certification
Based on Microsoft Learn: Architect AI Solutions For Business Productivity
"""

import os
import re
from datetime import datetime

# Module titles mapping
MODULE_TITLES = {
    "01": "Introduction to Agentic AI Business Solutions",
    "02": "Analyze Requirements for AI-Powered Business Solutions", 
    "03": "Design Overall AI Strategy for Business Solutions",
    "04": "Evaluate Costs and Benefits of AI Solutions",
    "05": "Design AI Agents for Business Solutions",
    "06": "Design Extensibility of AI Solutions",
    "07": "Orchestrate Configuration of Prebuilt Agents and Apps",
    "08": "Monitor, Analyze, and Tune AI Agents",
    "09": "Manage Testing AI-Powered Business Solutions",
    "10": "Design ALM Process for AI-Powered Business Solutions",
    "11": "Design Responsible AI Security, Governance, Risk Management, and Compliance"
}

def extract_key_content(markdown_content, module_num):
    """Extract key concepts, learning objectives, and important information from markdown"""
    
    # Extract learning objectives
    objectives_match = re.search(r'## Learning objectives\s*\n(.*?)(?=##|\Z)', markdown_content, re.DOTALL | re.IGNORECASE)
    objectives = objectives_match.group(1).strip() if objectives_match else ""
    
    # Extract prerequisites
    prereq_match = re.search(r'## Prerequisites\s*\n(.*?)(?=##|- \[|Take the|\Z)', markdown_content, re.DOTALL | re.IGNORECASE)
    prerequisites = prereq_match.group(1).strip() if prereq_match else ""
    
    # Extract unit titles (these often indicate key topics)
    units = re.findall(r'- \[([^\]]+)\]\([^)]+\)', markdown_content)
    
    return {
        'objectives': objectives,
        'prerequisites': prerequisites,
        'units': units
    }

def generate_html():
    """Generate interactive HTML study guide"""
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AB-100 Certification Study Guide - Architect AI Solutions For Business Productivity</title>
    <style>
        :root {{
            --primary-color: #0078d4;
            --secondary-color: #106ebe;
            --accent-color: #005a9e;
            --background-light: #f8f9fa;
            --text-dark: #242424;
            --text-medium: #484848;
            --border-color: #e0e0e0;
            --success-color: #107c10;
            --warning-color: #ffaa44;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        header h1 {{
            color: var(--primary-color);
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        header .subtitle {{
            color: var(--text-medium);
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .exam-info {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
        
        .info-badge {{
            background: var(--background-light);
            padding: 15px 25px;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }}
        
        .info-badge strong {{
            color: var(--primary-color);
            display: block;
            font-size: 1.1em;
        }}
        
        nav {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        nav h2 {{
            color: var(--text-dark);
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .module-nav {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }}
        
        .module-link {{
            display: block;
            padding: 15px 20px;
            background: var(--background-light);
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-dark);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .module-link:hover {{
            background: var(--primary-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,120,212,0.3);
        }}
        
        .module-link.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--accent-color);
        }}
        
        .module-number {{
            display: inline-block;
            background: var(--primary-color);
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            margin-right: 10px;
            font-weight: bold;
        }}
        
        .module-link:hover .module-number {{
            background: white;
            color: var(--primary-color);
        }}
        
        main {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .module-section {{
            display: none;
            animation: fadeIn 0.3s ease;
        }}
        
        .module-section.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .module-header {{
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .module-header h2 {{
            color: var(--primary-color);
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding: 25px;
            background: var(--background-light);
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }}
        
        .section h3 {{
            color: var(--secondary-color);
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section h3::before {{
            content: '📌';
        }}
        
        .section ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .section li {{
            padding: 10px 0;
            padding-left: 25px;
            position: relative;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .section li:last-child {{
            border-bottom: none;
        }}
        
        .section li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success-color);
            font-weight: bold;
        }}
        
        .key-concept {{
            background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
            padding: 20px;
            border-radius: 8px;
            border: 2px solid var(--warning-color);
            margin: 20px 0;
        }}
        
        .key-concept h4 {{
            color: #856404;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .key-concept h4::before {{
            content: '⭐';
        }}
        
        .quiz-section {{
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            padding: 25px;
            border-radius: 8px;
            border: 2px solid var(--success-color);
            margin-top: 30px;
        }}
        
        .quiz-section h3 {{
            color: #155724;
            margin-bottom: 20px;
        }}
        
        .quiz-question {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .quiz-question h4 {{
            color: var(--text-dark);
            margin-bottom: 15px;
        }}
        
        .quiz-options label {{
            display: block;
            padding: 12px 15px;
            background: var(--background-light);
            margin: 8px 0;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .quiz-options label:hover {{
            background: var(--primary-color);
            color: white;
        }}
        
        .quiz-options input[type="radio"] {{
            margin-right: 10px;
        }}
        
        .show-answer {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 10px;
            transition: background 0.3s ease;
        }}
        
        .show-answer:hover {{
            background: var(--secondary-color);
        }}
        
        .answer {{
            display: none;
            margin-top: 15px;
            padding: 15px;
            background: #d4edda;
            border-radius: 6px;
            border-left: 4px solid var(--success-color);
        }}
        
        .progress-tracker {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 1000;
            min-width: 250px;
        }}
        
        .progress-bar {{
            background: var(--background-light);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            background: linear-gradient(90deg, var(--success-color), #28a745);
            height: 100%;
            width: 0%;
            transition: width 0.5s ease;
            border-radius: 10px;
        }}
        
        .toc-section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .toc-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .toc-card {{
            background: var(--background-light);
            padding: 20px;
            border-radius: 8px;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
        }}
        
        .toc-card:hover {{
            border-color: var(--primary-color);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,120,212,0.15);
        }}
        
        .toc-card h4 {{
            color: var(--primary-color);
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        .toc-card ul {{
            list-style: none;
            font-size: 0.9em;
        }}
        
        .toc-card li {{
            padding: 5px 0;
            color: var(--text-medium);
        }}
        
        .toc-card li::before {{
            content: '• ';
            color: var(--primary-color);
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: white;
            margin-top: 30px;
        }}
        
        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .print-button:hover {{
            background: #0e630e;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                max-width: 100%;
            }}
            .progress-tracker, .print-button {{
                display: none;
            }}
            .module-section {{
                display: block !important;
                page-break-inside: avoid;
            }}
            header, main, nav, .toc-section {{
                box-shadow: none;
            }}
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}
            
            .exam-info {{
                flex-direction: column;
                align-items: center;
            }}
            
            .module-nav {{
                grid-template-columns: 1fr;
            }}
            
            main {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">📄 Print / Save as PDF</button>
    
    <div class="container">
        <header>
            <h1>🎯 AB-100 Certification Study Guide</h1>
            <p class="subtitle">Architect AI Solutions For Business Productivity</p>
            <p style="color: var(--text-medium); margin-top: 15px;">
                Complete interactive study material covering all 11 modules from Microsoft Learn
            </p>
            
            <div class="exam-info">
                <div class="info-badge">
                    <strong>📚 11 Modules</strong>
                    Comprehensive coverage
                </div>
                <div class="info-badge">
                    <strong>⏱️ Advanced Level</strong>
                    Solution Architect Role
                </div>
                <div class="info-badge">
                    <strong>🎓 Target Score</strong>
                    90%+ with 20% effort
                </div>
                <div class="info-badge">
                    <strong>📅 Updated</strong>
                    {datetime.now().strftime("%B %Y")}
                </div>
            </div>
        </header>
        
        <nav>
            <h2>📖 Quick Navigation</h2>
            <div class="module-nav">
'''
    
    # Add navigation links
    for mod_num, title in MODULE_TITLES.items():
        html_content += f'''                <a href="#module-{mod_num}" class="module-link" onclick="showModule('{mod_num}'); return false;">
                    <span class="module-number">{mod_num}</span>
                    {title[:50]}{'...' if len(title) > 50 else ''}
                </a>
'''
    
    html_content += '''            </div>
        </nav>
        
        <div class="toc-section">
            <h2 style="color: var(--primary-color); margin-bottom: 20px;">📋 Exam Focus Areas - The Vital 20%</h2>
            <p style="margin-bottom: 20px; color: var(--text-medium);">
                Based on Pareto Principle (80/20 rule), focus on these high-yield topics to achieve 90%+ score:
            </p>
            <div class="toc-grid">
'''
    
    # Add TOC cards for each module with key focus areas
    toc_data = {
        "01": ["AI Architect role & responsibilities", "Microsoft AI technologies overview", "Copilot solutions & business value", "Scaling AI across enterprise"],
        "02": ["AI agents for automation & analytics", "Grounding data quality (5 dimensions)", "Data organization for AI readiness", "Value assessment scenarios"],
        "03": ["Cloud Adoption Framework (CAF) phases", "Multi-agent solution design", "Build vs Buy vs Extend decisions", "Prompt engineering guidelines", "AI Center of Excellence"],
        "04": ["ROI criteria & TCO calculation", "Model routing strategies", "Cost-benefit analysis framework", "When to use custom models"],
        "05": ["Responsible AI principles", "Task vs Autonomous agents", "Copilot Studio design patterns", "Custom connectors integration", "Dynamics 365 Contact Center"],
        "06": ["Microsoft Foundry custom models", "Model Context Protocol (MCP)", "Agent extensibility patterns", "Computer Use capabilities", "Optimization for M365"],
        "07": ["Prebuilt Copilot configuration", "Finance & Supply Chain AI features", "Sales & Service orchestration", "Power Platform AI Hub"],
        "08": ["Monitoring frameworks", "Performance metrics & telemetry", "User feedback analysis", "AI-based diagnostic tools"],
        "09": ["Testing frameworks for AI agents", "Validation criteria for custom models", "End-to-end test scenarios", "Copilot for test case generation"],
        "10": ["ALM for datasets, prompts, models", "Environment governance", "Security across environments", "Dynamics 365 ALM processes"],
        "11": ["Responsible AI principles implementation", "Identity & access controls", "Prompt manipulation mitigations", "Audit trails & compliance", "Data residency requirements"]
    }
    
    for mod_num, topics in toc_data.items():
        html_content += f'''                <div class="toc-card">
                    <h4>Module {mod_num}: {MODULE_TITLES[mod_num][:40]}...</h4>
                    <ul>
'''
        for topic in topics:
            html_content += f'                        <li>{topic}</li>\n'
        html_content += '''                    </ul>
                </div>
'''
    
    html_content += '''            </div>
        </div>
        
        <main>
'''
    
    # Now add detailed module content
    for mod_num in range(1, 12):
        mod_str = str(mod_num).zfill(2)
        filename = f"/workspace/learning_materials/module{mod_str}.md"
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted = extract_key_content(content, mod_num)
            
            html_content += f'''
            <div id="module-{mod_str}" class="module-section {'active' if mod_num == 1 else ''}">
                <div class="module-header">
                    <h2>Module {mod_num}: {MODULE_TITLES[mod_str]}</h2>
                </div>
                
                <div class="section">
                    <h3>Learning Objectives</h3>
                    <ul>
'''
            # Parse objectives
            if extracted['objectives']:
                obj_items = re.findall(r'- (.+)', extracted['objectives'])
                for obj in obj_items[:8]:  # Limit to 8 objectives
                    html_content += f'                        <li>{obj}</li>\n'
            
            html_content += '''                    </ul>
                </div>
                
                <div class="section">
                    <h3>Key Topics Covered</h3>
                    <ul>
'''
            # Add unit topics
            for unit in extracted['units'][:10]:  # Limit to 10 units
                html_content += f'                        <li>{unit}</li>\n'
            
            html_content += '''                    </ul>
                </div>
                
                <div class="key-concept">
                    <h4>High-Yield Exam Topics</h4>
                    <p>Focus on understanding these concepts thoroughly:</p>
                    <ul>
'''
            # Add high-yield topics based on module
            high_yield_topics = {
                "01": [
                    "The AI architect's role in driving organizational transformation",
                    "Microsoft's AI technology stack: Azure AI, Copilot Studio, Power Platform",
                    "Out-of-box AI agents available in Microsoft ecosystem",
                    "Strategies for scaling AI adoption enterprise-wide"
                ],
                "02": [
                    "Five dimensions of grounding data quality: Accuracy, Relevance, Timeliness, Cleanliness, Availability",
                    "How AI agents support task automation vs data analytics vs decision-making",
                    "Criteria for assessing when AI adds measurable business value",
                    "Data organization patterns for AI consumption"
                ],
                "03": [
                    "Cloud Adoption Framework's 6 strategies: Plan, Ready, Adopt, Govern, Manage, Organize",
                    "When to build custom agents vs extend M365 Copilot vs use prebuilt",
                    "Decision criteria for custom AI model creation",
                    "Prompt library best practices and prompt engineering techniques",
                    "AI Center of Excellence components and governance"
                ],
                "04": [
                    "Total Cost of Ownership (TCO) components for AI solutions",
                    "ROI calculation methodology for AI-powered processes",
                    "Build vs Buy vs Extend decision framework",
                    "Model routing strategies for cost-performance optimization"
                ],
                "05": [
                    "Six Responsible AI principles: Fairness, Reliability, Privacy, Inclusiveness, Transparency, Accountability",
                    "Task agents vs Autonomous agents in Copilot Studio",
                    "Custom connector design for Dynamics 365 integration",
                    "Prompt-driven conversational agent patterns",
                    "Well-Architected Framework application to intelligent workloads"
                ],
                "06": [
                    "Microsoft Foundry capabilities for custom model deployment",
                    "Model Context Protocol (MCP) for agent extensibility",
                    "Computer Use feature for automating tasks across apps",
                    "Agent behaviors: reasoning modes, voice capabilities",
                    "Optimization strategies for Teams and SharePoint integration"
                ],
                "07": [
                    "Prebuilt Copilot agents for Finance, Supply Chain, Sales, Service",
                    "Configuration steps for operationalizing Copilot experiences",
                    "Process knowledge sources for in-app help",
                    "Interoperability patterns for cross-application agents"
                ],
                "08": [
                    "Key performance metrics for AI agents: accuracy, latency, user satisfaction",
                    "Telemetry data interpretation for model tuning",
                    "Backlog analysis techniques for continuous improvement",
                    "AI-based diagnostic tools for issue identification"
                ],
                "09": [
                    "Testing framework components for AI solutions",
                    "Validation criteria for custom AI models",
                    "End-to-end testing across multiple Dynamics 365 apps",
                    "Using Copilot to generate comprehensive test cases"
                ],
                "10": [
                    "ALM processes for prompts, datasets, and models",
                    "Environment strategy: Development, Test, Production",
                    "Governance and security controls across environments",
                    "Specific ALM considerations for Dynamics 365 Finance and Customer Experience"
                ],
                "11": [
                    "Responsible AI principles implementation in technical controls",
                    "Microsoft Entra ID and RBAC for AI agent security",
                    "Prompt injection attack vectors and mitigations",
                    "Data residency and sovereignty compliance requirements",
                    "Audit trail requirements for model and data changes"
                ]
            }
            
            for topic in high_yield_topics.get(mod_str, []):
                html_content += f'                        <li>{topic}</li>\n'
            
            html_content += '''                    </ul>
                </div>
'''
            
            # Add quiz questions for each module
            quiz_questions = {
                "01": [
                    {
                        "question": "Which of the following is NOT a core responsibility of an AI architect?",
                        "options": ["Aligning AI solutions with business goals", "Writing production code for all AI implementations", "Scaling AI adoption across the enterprise", "Identifying appropriate Microsoft AI services"],
                        "answer": "Writing production code for all AI implementations - Architects focus on design and strategy, not necessarily hands-on coding."
                    },
                    {
                        "question": "What are the three main categories of Microsoft AI solutions?",
                        "options": ["Azure AI Services, Microsoft Copilot, Power Platform AI", "Windows AI, Office AI, Cloud AI", "Basic AI, Advanced AI, Premium AI", "None of the above"],
                        "answer": "Azure AI Services, Microsoft Copilot, Power Platform AI - These represent Microsoft's comprehensive AI ecosystem."
                    }
                ],
                "02": [
                    {
                        "question": "Which is NOT one of the five dimensions of grounding data quality?",
                        "options": ["Accuracy", "Relevance", "Complexity", "Timeliness", "Availability"],
                        "answer": "Complexity - The five dimensions are Accuracy, Relevance, Timeliness, Cleanliness, and Availability."
                    },
                    {
                        "question": "AI agents are most valuable in which scenario?",
                        "options": ["Simple repetitive tasks only", "Complex decision-making with clear rules", "Tasks requiring human creativity exclusively", "Situations where data quality is poor"],
                        "answer": "Complex decision-making with clear rules - AI agents excel at processing large datasets and applying consistent logic."
                    }
                ],
                "03": [
                    {
                        "question": "What does CAF stand for in Microsoft's AI adoption framework?",
                        "options": ["Common Application Framework", "Cloud Adoption Framework", "Corporate AI Foundation", "Centralized Analytics Facility"],
                        "answer": "Cloud Adoption Framework - CAF provides proven guidance for AI adoption journey."
                    },
                    {
                        "question": "When should you consider building a custom AI model instead of using existing services?",
                        "options": ["Always build custom for better control", "When specific domain requirements aren't met by prebuilt models", "Never, always use prebuilt", "Only for small projects"],
                        "answer": "When specific domain requirements aren't met by prebuilt models - Custom models require significant investment and expertise."
                    }
                ],
                "04": [
                    {
                        "question": "TCO in AI solutions includes:",
                        "options": ["Only licensing costs", "Development, deployment, operation, and maintenance costs", "Just the initial development cost", "Hardware costs only"],
                        "answer": "Development, deployment, operation, and maintenance costs - TCO encompasses all costs throughout the solution lifecycle."
                    },
                    {
                        "question": "Model routing is primarily used to:",
                        "options": ["Increase complexity", "Optimize cost and performance by selecting appropriate models", "Reduce security", "Eliminate the need for testing"],
                        "answer": "Optimize cost and performance by selecting appropriate models - Route simple queries to smaller models, complex ones to larger models."
                    }
                ],
                "05": [
                    {
                        "question": "Which is NOT one of Microsoft's Responsible AI principles?",
                        "options": ["Fairness", "Profitability", "Transparency", "Accountability"],
                        "answer": "Profitability - The six principles are Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability."
                    },
                    {
                        "question": "Task agents in Copilot Studio are designed to:",
                        "options": ["Operate completely autonomously", "Complete specific, well-defined tasks", "Replace all human workers", "Work without any prompts"],
                        "answer": "Complete specific, well-defined tasks - Task agents handle defined workflows, while autonomous agents have broader capabilities."
                    }
                ],
                "06": [
                    {
                        "question": "What does MCP stand for in agent extensibility?",
                        "options": ["Microsoft Cloud Platform", "Model Context Protocol", "Multi-Channel Processing", "Machine Learning Core Protocol"],
                        "answer": "Model Context Protocol - MCP enables standardized communication between AI models and external tools/data sources."
                    },
                    {
                        "question": "Computer Use feature in Copilot Studio allows agents to:",
                        "options": ["Only analyze images", "Automate tasks across applications and websites", "Replace computers", "Use more computing power"],
                        "answer": "Automate tasks across applications and websites - Computer Use enables agents to interact with UIs like humans do."
                    }
                ],
                "07": [
                    {
                        "question": "Prebuilt Copilot agents are available for which Dynamics 365 applications?",
                        "options": ["Only Sales", "Finance, Supply Chain, Sales, Service", "Only Customer Service", "None"],
                        "answer": "Finance, Supply Chain, Sales, Service - Microsoft provides industry-specific prebuilt agents across D365 suite."
                    },
                    {
                        "question": "Process knowledge sources in Dynamics 365 Finance provide:",
                        "options": ["Financial reports only", "In-app contextual help and guidance", "External documentation links", "Video tutorials"],
                        "answer": "In-app contextual help and guidance - They deliver relevant information within the workflow context."
                    }
                ],
                "08": [
                    {
                        "question": "Key metrics for monitoring AI agents include:",
                        "options": ["Only response time", "Accuracy, latency, user satisfaction, completion rate", "Number of users only", "Server uptime only"],
                        "answer": "Accuracy, latency, user satisfaction, completion rate - Multiple metrics provide holistic view of agent performance."
                    },
                    {
                        "question": "Telemetry data is primarily used for:",
                        "options": ["Billing purposes", "Performance analysis and model tuning", "Marketing", "Employee monitoring"],
                        "answer": "Performance analysis and model tuning - Telemetry provides insights into actual usage patterns and issues."
                    }
                ],
                "09": [
                    {
                        "question": "Testing AI solutions requires validation of:",
                        "options": ["Only functional requirements", "Performance, safety, compliance, and accuracy", "Code syntax only", "User interface only"],
                        "answer": "Performance, safety, compliance, and accuracy - AI testing must cover multiple dimensions beyond traditional software testing."
                    },
                    {
                        "question": "End-to-end testing for AI solutions should include:",
                        "options": ["Individual component testing only", "Cross-application workflows and integrations", "Documentation review only", "User training only"],
                        "answer": "Cross-application workflows and integrations - E2E testing validates complete business processes across systems."
                    }
                ],
                "10": [
                    {
                        "question": "ALM stands for:",
                        "options": ["Automated Learning Machine", "Application Lifecycle Management", "Artificial Language Model", "Advanced Logic Module"],
                        "answer": "Application Lifecycle Management - ALM ensures consistent governance from development through production."
                    },
                    {
                        "question": "AI ALM processes must manage which components?",
                        "options": ["Only code", "Datasets, prompts, models, and configurations", "Only documentation", "Only user permissions"],
                        "answer": "Datasets, prompts, models, and configurations - AI solutions have unique artifacts requiring version control and governance."
                    }
                ],
                "11": [
                    {
                        "question": "Which is a common prompt manipulation attack?",
                        "options": ["Prompt injection", "Prompt encryption", "Prompt compression", "Prompt formatting"],
                        "answer": "Prompt injection - Attackers inject malicious instructions to override intended behavior."
                    },
                    {
                        "question": "Data residency requirements refer to:",
                        "options": ["Where data can be stored geographically", "Who can access data", "How long data is retained", "Data format standards"],
                        "answer": "Where data can be stored geographically - Regulations may require data to remain within specific jurisdictions."
                    }
                ]
            }
            
            if mod_str in quiz_questions:
                html_content += '''
                <div class="quiz-section">
                    <h3>📝 Practice Questions</h3>
'''
                for i, q in enumerate(quiz_questions[mod_str], 1):
                    html_content += f'''
                    <div class="quiz-question">
                        <h4>Question {i}: {q["question"]}</h4>
                        <div class="quiz-options">
'''
                    for j, opt in enumerate(q["options"]):
                        html_content += f'''                            <label>
                                <input type="radio" name="q{mod_str}_{i}" value="{j}">
                                {opt}
                            </label>
'''
                    html_content += f'''                        </div>
                        <button class="show-answer" onclick="toggleAnswer('ans_{mod_str}_{i}')">Show Answer</button>
                        <div id="ans_{mod_str}_{i}" class="answer">
                            <strong>Correct Answer:</strong> {q["answer"]}
                        </div>
                    </div>
'''
                html_content += '''                </div>
'''
            
            html_content += '''        </div>
'''
            
        except FileNotFoundError:
            print(f"Warning: Module {mod_str} file not found")
    
    html_content += '''        </main>
        
        <footer>
            <p>© 2025 AB-100 Study Guide | Based on Microsoft Learn Content</p>
            <p>Last Updated: ''' + datetime.now().strftime("%B %d, %Y") + '''</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                This study guide is designed to help you prepare for the AB-100 certification exam. 
                Focus on the highlighted key concepts and practice questions for optimal results.
            </p>
        </footer>
        
        <div class="progress-tracker">
            <strong>📊 Study Progress</strong>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Modules Completed: <span id="modulesCompleted">0</span>/11
            </p>
        </div>
    </div>
    
    <script>
        function showModule(moduleNum) {
            // Hide all sections
            document.querySelectorAll('.module-section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show selected section
            const targetSection = document.getElementById('module-' + moduleNum);
            if (targetSection) {
                targetSection.classList.add('active');
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            
            // Update navigation
            document.querySelectorAll('.module-link').forEach(link => {
                link.classList.remove('active');
            });
            event.target.closest('.module-link').classList.add('active');
            
            // Track progress
            updateProgress();
        }
        
        function toggleAnswer(answerId) {
            const answer = document.getElementById(answerId);
            if (answer) {
                answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
            }
        }
        
        function updateProgress() {
            const completed = new Set();
            document.querySelectorAll('.module-section.active').forEach(section => {
                const moduleId = section.id.replace('module-', '');
                completed.add(moduleId);
            });
            
            const percentage = (completed.size / 11) * 100;
            document.getElementById('progressFill').style.width = percentage + '%';
            document.getElementById('modulesCompleted').textContent = completed.size;
        }
        
        // Initialize first module as active
        document.addEventListener('DOMContentLoaded', function() {
            updateProgress();
        });
        
        // Track reading time for engagement
        let timeSpent = 0;
        setInterval(() => {
            timeSpent++;
            console.log('Study time: ' + Math.floor(timeSpent / 60) + ' minutes');
        }, 1000);
    </script>
</body>
</html>
'''
    
    return html_content

def generate_pdf_content():
    """Generate simplified content optimized for PDF export"""
    
    pdf_content = f"""# AB-100 Certification Study Guide
## Architect AI Solutions For Business Productivity

**Generated:** {datetime.now().strftime("%B %d, %Y")}

---

## Executive Summary

This study guide covers the essential 20% of content needed to achieve 90%+ on the AB-100 certification exam, following the Pareto Principle. Focus on the highlighted key concepts, learning objectives, and practice questions.

### Exam Overview
- **Level:** Advanced
- **Role:** Solution Architect  
- **Modules:** 11
- **Products:** Microsoft 365 Copilot, Power Platform, Copilot Studio, Dynamics 365

---

## Table of Contents

"""
    
    for mod_num, title in MODULE_TITLES.items():
        pdf_content += f"- Module {mod_num}: {title}\n"
    
    pdf_content += "\n---\n\n"
    
    # Add detailed content for each module
    for mod_num in range(1, 12):
        mod_str = str(mod_num).zfill(2)
        filename = f"/workspace/learning_materials/module{mod_str}.md"
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted = extract_key_content(content, mod_num)
            
            pdf_content += f"""
# Module {mod_num}: {MODULE_TITLES[mod_str]}

## Learning Objectives
"""
            if extracted['objectives']:
                obj_items = re.findall(r'- (.+)', extracted['objectives'])
                for obj in obj_items:
                    pdf_content += f"- {obj}\n"
            
            pdf_content += f"""
## Key Topics
"""
            for unit in extracted['units']:
                pdf_content += f"- {unit}\n"
            
            # Add high-yield exam tips
            high_yield_tips = {
                "01": """
## ⭐ High-Yield Exam Focus
- Understand the AI architect's strategic role vs technical implementation
- Know Microsoft's AI service categories: Azure AI, Copilot, Power Platform
- Memorize out-of-box AI agents available in Microsoft ecosystem
- Review scaling strategies for enterprise AI adoption
""",
                "02": """
## ⭐ High-Yield Exam Focus
- MEMORIZE the 5 dimensions of grounding data quality: Accuracy, Relevance, Timeliness, Cleanliness, Availability
- Understand when AI agents add measurable value vs when they don't
- Know data organization patterns for AI consumption
- Differentiate between task automation, analytics, and decision-making use cases
""",
                "03": """
## ⭐ High-Yield Exam Focus
- Cloud Adoption Framework phases: Plan, Ready, Adopt, Govern, Manage, Organize
- Build vs Buy vs Extend decision criteria (critical exam topic)
- When to create custom AI models vs use prebuilt
- Prompt engineering best practices and techniques
- AI Center of Excellence components
""",
                "04": """
## ⭐ High-Yield Exam Focus
- TCO components for AI solutions (development, deployment, operations, maintenance)
- ROI calculation methodology
- Model routing strategies for cost optimization
- Decision framework for build/buy/extend
""",
                "05": """
## ⭐ High-Yield Exam Focus
- SIX Responsible AI principles: Fairness, Reliability & Safety, Privacy & Security, Inclusiveness, Transparency, Accountability
- Task agents vs Autonomous agents differences
- Copilot Studio design patterns
- Custom connector integration approaches
- Well-Architected Framework application
""",
                "06": """
## ⭐ High-Yield Exam Focus
- Microsoft Foundry capabilities
- Model Context Protocol (MCP) purpose and benefits
- Computer Use feature capabilities
- Agent optimization for M365 (Teams, SharePoint)
- Extensibility patterns
""",
                "07": """
## ⭐ High-Yield Exam Focus
- Prebuilt Copilot agents for Finance, Supply Chain, Sales, Service
- Configuration and operationalization steps
- Process knowledge sources
- Cross-application interoperability
""",
                "08": """
## ⭐ High-Yield Exam Focus
- Key performance metrics: accuracy, latency, satisfaction, completion rate
- Telemetry interpretation for tuning
- User feedback analysis techniques
- AI diagnostic tools
""",
                "09": """
## ⭐ High-Yield Exam Focus
- Testing framework components
- Validation criteria for custom models
- End-to-end testing across D365 apps
- Using Copilot for test generation
""",
                "10": """
## ⭐ High-Yield Exam Focus
- ALM for prompts, datasets, models (unique AI artifacts)
- Environment strategy (Dev/Test/Prod)
- Governance and security across environments
- D365-specific ALM considerations
""",
                "11": """
## ⭐ High-Yield Exam Focus
- Responsible AI implementation in technical controls
- Microsoft Entra ID and RBAC for AI security
- Prompt injection attacks and mitigations (critical!)
- Data residency and compliance requirements
- Audit trail requirements
"""
            }
            
            if mod_str in high_yield_tips:
                pdf_content += high_yield_tips[mod_str]
            
            pdf_content += "\n---\n\n"
            
        except FileNotFoundError:
            print(f"Warning: Module {mod_str} file not found")
    
    # Add practice exam section
    pdf_content += """
# Practice Exam Questions

## Module 1: Introduction
**Q1.** Which is NOT a core AI architect responsibility?
- A) Aligning AI with business goals
- B) Writing all production code
- C) Scaling AI adoption
- D) Identifying appropriate services

**Answer:** B - Architects focus on strategy and design, not necessarily hands-on coding.

**Q2.** What are Microsoft's three main AI solution categories?
- A) Azure AI Services, Microsoft Copilot, Power Platform AI
- B) Windows AI, Office AI, Cloud AI
- C) Basic, Advanced, Premium AI
- D) None of the above

**Answer:** A - These represent Microsoft's comprehensive AI ecosystem.

## Module 2: Requirements Analysis
**Q3.** Which is NOT a dimension of grounding data quality?
- A) Accuracy
- B) Relevance  
- C) Complexity
- D) Timeliness

**Answer:** C - The five dimensions are Accuracy, Relevance, Timeliness, Cleanliness, Availability.

## Module 3: AI Strategy
**Q4.** What does CAF stand for?
- A) Common Application Framework
- B) Cloud Adoption Framework
- C) Corporate AI Foundation
- D) Centralized Analytics Facility

**Answer:** B - Cloud Adoption Framework provides proven AI adoption guidance.

**Q5.** When should you build a custom AI model?
- A) Always for better control
- B) When prebuilt models don't meet specific requirements
- C) Never, always use prebuilt
- D) Only for small projects

**Answer:** B - Custom models require significant investment; use when prebuilt options are insufficient.

## Module 4: Cost-Benefit Analysis
**Q6.** TCO for AI solutions includes:
- A) Only licensing costs
- B) Development, deployment, operations, maintenance
- C) Just initial development
- D) Hardware only

**Answer:** B - TCO encompasses all lifecycle costs.

## Module 5: AI Agent Design
**Q7.** Which is NOT a Responsible AI principle?
- A) Fairness
- B) Profitability
- C) Transparency
- D) Accountability

**Answer:** B - The six principles are Fairness, Reliability, Privacy, Inclusiveness, Transparency, Accountability.

## Module 6: Extensibility
**Q8.** What does MCP stand for?
- A) Microsoft Cloud Platform
- B) Model Context Protocol
- C) Multi-Channel Processing
- D) Machine Learning Core

**Answer:** B - Model Context Protocol enables standardized AI tool communication.

## Module 7: Prebuilt Agents
**Q9.** Prebuilt Copilots are available for:
- A) Only Sales
- B) Finance, Supply Chain, Sales, Service
- C) Only Customer Service
- D) None

**Answer:** B - Microsoft provides prebuilt agents across the D365 suite.

## Module 8: Monitoring
**Q10.** Key AI agent metrics include:
- A) Only response time
- B) Accuracy, latency, satisfaction, completion rate
- C) User count only
- D) Server uptime only

**Answer:** B - Multiple metrics provide holistic performance view.

## Module 9: Testing
**Q11.** AI testing must validate:
- A) Only functional requirements
- B) Performance, safety, compliance, accuracy
- C) Code syntax only
- D) UI only

**Answer:** B - AI testing covers multiple dimensions beyond traditional software testing.

## Module 10: ALM
**Q12.** ALM stands for:
- A) Automated Learning Machine
- B) Application Lifecycle Management
- C) Artificial Language Model
- D) Advanced Logic Module

**Answer:** B - ALM ensures governance from development through production.

## Module 11: Security & Compliance
**Q13.** A common prompt attack is:
- A) Prompt injection
- B) Prompt encryption
- C) Prompt compression
- D) Prompt formatting

**Answer:** A - Prompt injection overrides intended behavior with malicious instructions.

**Q14.** Data residency refers to:
- A) Geographic storage restrictions
- B) Access permissions
- C) Retention periods
- D) Format standards

**Answer:** A - Regulations may require data to remain within specific jurisdictions.

---

## Quick Reference: Critical Concepts to Memorize

### Responsible AI Principles (6)
1. Fairness
2. Reliability & Safety
3. Privacy & Security
4. Inclusiveness
5. Transparency
6. Accountability

### Grounding Data Quality Dimensions (5)
1. Accuracy
2. Relevance
3. Timeliness
4. Cleanliness
5. Availability

### Cloud Adoption Framework Strategies (6)
1. Plan
2. Ready
3. Adopt
4. Govern
5. Manage
6. Organize

### Key Decision Points
- **Build vs Buy vs Extend:** Evaluate based on unique requirements, cost, time-to-market
- **Custom Model vs Prebuilt:** Custom when domain-specific needs aren't met
- **Task vs Autonomous Agents:** Task for defined workflows, autonomous for broader capabilities

---

## Study Tips for 90%+ Score

1. **Focus on Understanding, Not Memorization:** Understand WHY certain approaches are recommended
2. **Practice Scenarios:** Apply concepts to real-world business situations
3. **Review Microsoft Documentation:** Supplement with official docs for latest updates
4. **Take Practice Tests:** Use the questions in this guide and seek additional practice exams
5. **Join Study Groups:** Discuss concepts with other candidates
6. **Hands-on Practice:** Use trial versions of Copilot Studio, Power Platform
7. **Review Exam Skills Outline:** Ensure you've covered all official exam objectives

---

*This study guide is based on Microsoft Learn content for the AB-100 certification path. 
Always verify with official Microsoft documentation for the most current information.*
"""
    
    return pdf_content

if __name__ == "__main__":
    # Generate HTML
    html_content = generate_html()
    with open("/workspace/AB100_Study_Guide.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ Generated interactive HTML study guide: AB100_Study_Guide.html")
    
    # Generate PDF-ready Markdown
    pdf_content = generate_pdf_content()
    with open("/workspace/AB100_Study_Guide.md", "w", encoding="utf-8") as f:
        f.write(pdf_content)
    print("✓ Generated PDF-ready Markdown: AB100_Study_Guide.md")
    
    print("\n📚 Study materials generated successfully!")
    print("   - Open AB100_Study_Guide.html in a browser for interactive learning")
    print("   - Convert AB100_Study_Guide.md to PDF using any Markdown to PDF converter")
    print("   - Or use the Print function in browser to save HTML as PDF")
