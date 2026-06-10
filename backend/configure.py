# ==========================================
# KNOWLEDGE BASE MAPPING CONFIGURATION
# ==========================================

# This file determines which embedding JSON files are loaded for a given query.
# The `resolve_files` function uses the frontend parameters (Year, Branch, Semester, Subject)
# to find the correct files based on the ACADEMIC_CONFIG structure.

import os

ACADEMIC_CONFIG = {
   
    "Bachelor of Commerce (Accounting & Finance)": {
        "1st Year": {
            "Semester 1": {
                "Principles of Financial Accounting": [
                    {"title": "Introduction to Financial Accounting", "file": "No_images_dataBCOMAF/Financial Accounting.pdf.json"},
                    {"title": "Financial Accounting (ICAI)", "file": "No_images_dataBCOMAF/Financial Accounting ICAI.pdf.json"},
                    {"title": "Financial Accounting (Maheshwari)", "file": "No_images_dataBCOMAF/Document from Arunkumar Chandrasekaar.pdf.json"},
                    {"title": "Financial Accounting - BMS", "file": "No_images_dataBCOMAF/Financial Accounting - BMS .pdf.json"}
                ],
                "Business Management": [
                    {"title": "Principles and Practices of Management (LPU)", "file": "No_images_dataBCOMAF/DCOM102_DMGT101_PRINCIPLES_AND_PRACTICES_OF_MANAGEMENT.pdf.json"},
                    {"title": "Principles of Business Management", "file": "No_images_dataBCOMAF/e.book_Principles of Management.pdf.json"},
                    {"title": "Principles of Management(P C TRIPATHI, P N REDDY)", "file": "No_images_dataBCOMAF/Principles of management (P C Tripathi, P N Reddy) (Z-Library).pdf.json"},
                    {"title": "Principles of Management", "file": "No_images_dataBCOMAF/Principle-Of-Management.pdf.json"},
                ],
                "Business Statistics & Operations": [
                    {"title": "Business Mathematics and Statistics (Das)", "file": "No_images_dataBCOMAF/Business Mathematics and Statistics (N Das Dr. J K Das) (Z-Library).pdf.json"},
                    {"title": "Business Mathematics, Logical Reasoning and Statistics (ICAI)", "file": "No_images_dataBCOMAF/BUSINESS MATHEMATICS, LOGICAL REASONING AND STATISTICS (BOARD OF STUDIES ICAI) (Z-Library).pdf.json"},
                    {"title": "Business Statistics (Alagar)", "file": "No_images_dataBCOMAF/Business Statistics (K. Alagar) (Z-Library).pdf.json"}
                ]
            },
            "Semester 2": {
                "Advanced Financial Accounting": [
                    {"title": "Advanced Accounting (Maheshwari)", "file": "No_images_dataBCOMAF/ADVANCED ACCOUNTING_3461.pdf.json"},
                    {"title": "Advanced Financial Accounting", "file": "No_images_dataBCOMAF/Advanced Financial Accounting.pdf.json"},
                    {"title": "Advanced FA", "file": "No_images_dataBCOMAF/Advanced FA.pdf.json"}
                ],
                "Banking & Financial System": [
                    {"title": "Banking Theory, Law and Practice (Gordon)", "file": "No_images_dataBCOMAF/Banking Theory, Law and Practice (E. Gordon K. Natarajan) (Z-Library).pdf.json"},
                    {"title": "Management of Banking and Financial Services (Suresh)", "file": "No_images_dataBCOMAF/Management of Banking and Financial Services (Padmalatha Suresh, Justin Paul) (Z-Library).pdf.json"},
                    {"title": "Negotiable Instruments, Banking and Insurance (Goyal)", "file": "No_images_dataBCOMAF/NEGOTIABLE INSTRUMENTS, BANKING AND INSURANCE (For LL.B. Students of various Universities of India and Civil Judicial… (B.K. GOYAL) (Z-Library).pdf.json"},
                    {"title": "Trade Finance and Foreign Exchange(TFFE)", "file": "No_images_dataBCOMAF/Trade Finance and Foreign Exchange (TFFE) (1).pdf.json"}
                ],
                "Business Arithmetic & Logical": [
                    {"title": "Business Mathematics, Logical Reasoning and Statistics (ICAI)", "file": "No_images_dataBCOMAF/BUSINESS MATHEMATICS, LOGICAL REASONING AND STATISTICS (BOARD OF STUDIES ICAI) (Z-Library).pdf.json"}
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                "Corporate Accounting": [
                    {"title": "Corporate Accounting (Rajasekaran)", "file": "No_images_dataBCOMAF/Corporate Accounting  for B. Com course of Uttar Pradesh Universities (V. Rajasekaran) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (Hanif)", "file": "No_images_dataBCOMAF/Corporate Accounting (M Hanif A Mukherjee) (Z-Library) (1).pdf.json"},
                    {"title": "Corporate Accounting (Radhika)", "file": "No_images_dataBCOMAF/Corporate Accounting (P. Radhika Anita Raman) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (Rajasekaran/Lalitha)", "file": "No_images_dataBCOMAF/Corporate Accounting (V. Rajasekaran, R. Lalitha) (Z-Library).pdf.json"},
                    {"title": "Document from Arunkumar Chandra Sekhar", "file": "No_images_dataBCOMAF/Document from Arunkumar Chandrasekaar.pdf.json"},
                ],
                "International Accounting Standards and Reporting": [
                    {"title": "Advanced Accounting (ICAI)", "file": "No_images_dataBCOMAF/ADVANCED ACCOUNTING_3461.pdf.json"},
                    {"title": "International GAAP 2021", "file": "No_images_dataBCOMAF/IFRS_merged (1).pdf.json"},
                    {"title": "Wiley Interpretation and Application of IFRS Standards 2023", "file": "No_images_dataBCOMAF/Wiley 2023 Interpretation and Application of IFRS Standards (P. K. F. PKF Internation) (Z-Library).pdf.json"},
                    {"title": "Interpretation and Application of IFRS", "file": "No_images_dataBCOMAF/IFRS.pdf.json"}
                ],
                "Foreign Exchange & Financing for Foreign Trade": [
                    {"title": "International Trade and Finance (Natarajan)", "file": "No_images_dataBCOMAF/3InternationalTradeandFinance.pdf.json"},
                    {"title": "Trade Finance & Foreign Exchange (Habib)", "file": "No_images_dataBCOMAF/Trade Finance and Foreign Exchange (TFFE).pdf.json"},
                    {"title": "Forex", "file": "No_images_dataBCOMAF/Forex.pdf.json"},
                    {"title": "316CO21", "file": "No_images_dataBCOMAF/316CO21.pdf.json"}, 
                ],
                "Accounting for Decision Making": [
                    {"title": "Accountancy and Financial Management-I (Sonawane)", "file": "No_images_dataBCOMAF/Accountancy and Financial Management–I (Sanjay D. Sonawane) (Z-Library).pdf.json"},
                    {"title": "Accounting for Managers (Rajasekaran)", "file": "No_images_dataBCOMAF/Accounting For Managers (For VTU) (V. Rajasekaran) (Z-Library).pdf.json"},
                    {"title": "Financial Accounting for Management (Ramachandran)", "file": "No_images_dataBCOMAF/Financial Accounting For Management (Ramachandran And K Ramkumar) (Z-Library).pdf.json"}
                ],
                "Business & Corporate Law": [
                    {"title": "Business Law", "file": "No_images_dataBCOMAF/Business Law.pdf.json"},
                    {"title": "Business Law (icmai)", "file": "No_images_dataBCOMAF/Business Law icmai.pdf.json"},
                    {"title": "Business Law (PY Univ)", "file": "No_images_dataBCOMAF/Business Law PY Univ.pdf.json"},
                    {"title": "Company Law", "file": "No_images_dataBCOMAF/CompanyLaw_BOOK.pdf.json"},
                    {"title": "Corporate Law (ICMAI)", "file": "No_images_dataBCOMAF/Corporate law ICMAI.pdf.json"},
                    {"title": "Corporate and Business Laws", "file": "No_images_dataBCOMAF/CORPORATE_AND_BUSINESS_LAWS.pdf.json"}
                ]
            },
            "Semester 4": {
                "Advanced Corporate Accounting": [
                    {"title": "Corporate Accounting (Rajasekaran)", "file": "No_images_dataBCOMAF/Corporate Accounting  for B. Com course of Uttar Pradesh Universities (V. Rajasekaran) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (Hanif)", "file": "No_images_dataBCOMAF/Corporate Accounting (M Hanif A Mukherjee) (Z-Library) (1).pdf.json"},
                    {"title": "Corporate Accounting (Radhika)", "file": "No_images_dataBCOMAF/Corporate Accounting (P. Radhika Anita Raman) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (Rajasekaran/Lalitha)", "file": "No_images_dataBCOMAF/Corporate Accounting (V. Rajasekaran, R. Lalitha) (Z-Library).pdf.json"},
                    {"title": "Document from Arunkumar Chandra Sekhar", "file": "No_images_dataBCOMAF/Document from Arunkumar Chandrasekaar.pdf.json"},
                ],
                "Indirect Taxation": [
                    {"title": "Indirect Tax Reform in India (Sinha)", "file": "No_images_dataBCOMAF/Indirect Tax Reform in India 1947 To GST and Beyond (Sinha, Yashwant, Srivastava, Vinay K.) (Z-Library).pdf.json"},
                    {"title": "Indirect Taxation", "file": "No_images_dataBCOMAF/Indirect Taxation.pdf.json"}
                ],
                "Principles of Financial Management": [
                    {"title": "Fundamentals of Financial Management", "file": "No_images_dataBCOMAF/Fundamentals of Financial Management.pdf.json"},
                    {"title": "Advanced Financial Management", "file": "No_images_dataBCOMAF/Advanced Financial Management.pdf.json"}
                ],
                "Fiscal Economics": [
                    {"title": "Fiscal Economics", "file": "No_images_dataBCOMAF/Fiscal Economics.pdf.json"},
                    {"title": "Eco-Fiscal Economics", "file": "No_images_dataBCOMAF/SLM - 19357 - Eco-Fiscal Economics.pdf.pdf.json"}
                ],
                "Auditing – Theory & Applications": [
                    {"title": "Auditing and Assurance (Basu)", "file": "No_images_dataBCOMAF/Auditing and assurance explains the concepts, principles and techniques of auditing (Basu, Sanjib Kumar) (Z-Library) (1).pdf.json"},
                    {"title": "Auditing Principles and Practices (Sana)", "file": "No_images_dataBCOMAF/Auditing Principles and Practices (Ashish Kumar Sana, Swapan Sarkar etc.) (Z-Library) (1).pdf.json"},
                    {"title": "Auditing Principles and Techniques (Basu)", "file": "No_images_dataBCOMAF/Auditing Principles and Techniques (Sanjib Kumar Basu) (Z-Library).pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "Advanced Financial Management": [
                    {"title": "Advanced Financial Management", "file": "No_images_dataBCOMAF/Advanced Financial Management.pdf.json"}
                ],
                "Principles of Cost Accounting": [
                    {"title": "Cost Accounting (Jawahar Lal)", "file": "No_images_dataBCOMAF/Cost accounting (Jawahar Lal Seema Srivastava) (Z-Library).pdf.json"},
                    {"title": "Financial Cost and Management Accounting (Periasami)", "file": "No_images_dataBCOMAF/Textbook of Financial Cost and Management Accounting (Periasami P.) (Z-Library).pdf.json"}
                ],
                "Direct Taxes - I": [
                    {"title": "Direct Taxes", "file": "No_images_dataBCOMAF/Direct Taxes.pdf.json"},
                    {"title": "Taxation", "file": "No_images_dataBCOMAF/taxation.pdf.json"},
                    {"title": "Direct_Tax_Laws_International_Taxation", "file": "No_images_dataBCOMAF/Direct_Tax_Laws_International_Taxation.pdf.json"},
                    {"title": "Income Tax-I (Rajesh Kumar)", "file": "No_images_dataBCOMAF/Income Tax-I (V. Rajesh Kumar R. K. Sreekantha) (Z-Library).pdf.json"},
                    {"title": "Students' Guide to Income Tax (Singhania)", "file": "No_images_dataBCOMAF/Taxmann Students Guide to Income Tax Including GST (Vinod K. Singhania, Monica Singhania) (Z-Library).pdf.json"}
                ],
                "Computerized Accounting": [
                    {"title": "Tally ERP 9 At A Glance", "file": "No_images_dataBCOMAF/Tally ERP 9 At A Glance (Tally) (Z-Library).pdf.json"},
                    {"title": "Mastering Tally PRIME", "file": "No_images_dataBCOMAF/Mastering Tally PRIME Training, Certification  Job (ASOK K. NADHANI) (Z-Library).pdf.json"},
                    {"title": "Tally ERP 9 + GST Implementation", "file": "No_images_dataBCOMAF/Tally ERP 9 + GST Implementation Voucher Entries, Inventory Management, Order Processing, Taxation, and GST Accounting (Akshay Rajgaria) (Z-Library).pdf.json"}
                ],
                "Research Methodology": [
                    {"title": "Management Research Methodology", "file": "No_images_dataBCOMAF/Management Research Methodology Integration of Principles, Methods and Techniques ( etc.) (Z-Library).pdf.json"},
                    {"title": "Research Methodology Methods and Techniques (Kothari)", "file": "No_images_dataBCOMAF/Research Methodology - Methods and Techniques (C.R. Kothari) (Z-Library).pdf.json"},
                    {"title": "Research Methodology (Ranjit Kumar)", "file": "No_images_dataBCOMAF/Research Methodology. (Kumar, Ranjit) (Z-Library).pdf.json"}
                ]
            },
            "Semester 6": {
                "Advanced Cost Accounting": [
                    {"title": "Cost Accounting (Jawahar Lal)", "file": "No_images_dataBCOMAF/Cost accounting (Jawahar Lal Seema Srivastava) (Z-Library).pdf.json"},
                    {"title": "Financial Cost and Management Accounting (Periasami)", "file": "No_images_dataBCOMAF/Textbook of Financial Cost and Management Accounting (Periasami P.) (Z-Library).pdf.json"}
                ],
                "Investment Management": [
                    {"title": "Investment Management (Avadhani)", "file": "No_images_dataBCOMAF/Investment Management (V.A. Avadhani) (Z-Library).pdf.json"},
                    {"title": "Investment Management (Hiriyappa)", "file": "No_images_dataBCOMAF/Investment Management Securities and Portfolio Management (Dr. B. Hiriyappa) (Z-Library).pdf.json"}
                ],
                "Direct Taxes - II": [
                    {"title": "Direct Taxes", "file": "No_images_dataBCOMAF/Direct Taxes.pdf.json"},
                    {"title": "Income Tax-I (Rajesh Kumar)", "file": "No_images_dataBCOMAF/Income Tax-I (V. Rajesh Kumar R. K. Sreekantha) (Z-Library).pdf.json"},
                    {"title": "Students' Guide to Income Tax (Singhania)", "file": "No_images_dataBCOMAF/Taxmann Students Guide to Income Tax Including GST (Vinod K. Singhania, Monica Singhania) (Z-Library).pdf.json"}
                ],
                "Management of Lending": [
                    {"title": "Managing Lending Operations", "file": "No_images_dataBCOMAF/(38)-managing of lending-operations.pdf.json"},
                    {"title": "Credit Analysis and Lending Management", "file": "No_images_dataBCOMAF/Credit Analysis and Lending Management (Milind Sathye, James Bartle) (Z-Library).pdf.json"},
                    {"title": "Credit Risk Analysis (Ciby Joseph)", "file": "No_images_dataBCOMAF/Credit Risk Analysis - A tryst with strategic prudence (Ciby Joseph) (Z-Library).pdf.json"},
                    {"title": "Credit Risk Management (Baesens)", "file": "No_images_dataBCOMAF/Credit Risk Management Basic Concepts financial risk components, rating analysis, models, economic and regulatory capital (Baesens B., Van Gestel T.) (Z-Library).pdf.json"},
                    {"title": "Management of Lending Activities (Lec 31)", "file": "No_images_dataBCOMAF/lec31.pdf.json"},
                    {"title": "Management of Lending Activities (Lec 37)", "file": "No_images_dataBCOMAF/lec37.pdf.json"}
                ],
                "International Financial Management": [
                    {"title": "International Financial Management (LPU)", "file": "No_images_dataBCOMAF/DMGT549_INTERNATIONAL_FINANCIAL_MANAGEMENT.pdf.json"},
                    {"title": "International Financial Management (Bekaert)", "file": "No_images_dataBCOMAF/Geert_Bekaert_Robert_J_Hodrick_International_Financial_Management.pdf.json"}
                ]
            }
        }
    },
    "Bachelor of Commerce (General)": {
        "1st Year": {
            "Semester 1": {
                "Financial Accounting - I": [
                    {"title": "Advanced Accounting", "file": "No_images_dataBCOMGEN/Copy of ADVANCED ACCOUNTING.pdf.json"},
                    {"title": "Financial Accounting (Jain & Narang)", "file": "No_images_dataBCOMGEN/Copy of Accounting jain-and-narang.pdf.json"},
                    {"title": "Financial Accounting Part A", "file": "No_images_dataBCOMGEN/Financial Acconting Part A.pdf.json"},
                    {"title": "Financial Accounting Part B", "file": "No_images_dataBCOMGEN/Financial Acconting Part B.pdf.json"},
                ],
                "Quantitative Techniques": [
                     {"title": "Operations Research (Sharma)", "file": "No_images_dataBCOMGEN/Operations-research j k sharma.pdf.json"},
                     {"title": "Operations Research (Hira & Gupta)", "file": "No_images_dataBCOMGEN/Operations Research Hira and Gupta.pdf.json"},
                     {"title": "Optimization Methods in Finance", "file": "No_images_dataBCOMGEN/Optimization_Methods_in_Finance.pdf.json"},
                     {"title": "Quantative Technique", "file": "No_images_dataBCOMGEN/Quantitative Techniques.pdf.json"},
                ],
                "Business Economics":[
                    {"title": "Business Economics", "file": "No_images_dataBCOMGEN/Business Economics.pdf.json"},
                ],
                
            },
            "Semester 2": {
                "Development Economics": [
                    {"title": "Development Economics", "file": "No_images_dataBCOMGEN/Development Economics.pdf.json"},
                    {"title": "Economics of Growth", "file": "No_images_dataBCOMGEN/Economics of Growth and Develpoment.pdf.json"}
                ],
                "Quantitative Techniques":[
                    {"title": "Business Statistic by S_Gupta", "file": "No_images_dataBCOMGEN/Business Statistics by S_P_Gupta_M_P_Gupta.pdf.json"},
                    {"title": "Operations Research (Hira & Gupta)", "file": "No_images_dataBCOMGEN/Operations Research Hira and Gupta.pdf.json"},
                    {"title": "Operations Research (Sharma)", "file": "No_images_dataBCOMGEN/Operations-research j k sharma.pdf.json"},
                    {"title": "Optimization Methods in Finance", "file": "No_images_dataBCOMGEN/Optimization_Methods_in_Finance.pdf.json"},
                     {"title": "Quantative Technique", "file": "No_images_dataBCOMGEN/Quantitative Techniques.pdf.json"},
                ],
                "Financial Accounting - II": [
                    {"title": "Advanced Accounting", "file": "No_images_dataBCOMGEN/Copy of ADVANCED ACCOUNTING.pdf.json"},
                    {"title": "Financial Accounting (Jain & Narang)", "file": "No_images_dataBCOMGEN/Copy of Accounting jain-and-narang.pdf.json"},
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                 "CORPORATE ACCOUNTING I ": [
                    {"title": "Corporate Accounting", "file": "No_images_dataBCOMGEN/Corporate-Accounting 2.pdf.json"}
                 ],
                 "Banking Theory": [
                    {"title": "Banking Theory, Law and Practice", "file": "No_images_dataBCOMGEN/Banking Theory, Law and Practice (E. Gordon K. Natarajan) (Z-Library).pdf.json"}
                 ],
                 "Corporate Governance": [
                    {"title": "Corporate Governance & Ethics", "file": "No_images_dataBCOMGEN/CORPORATE_GOVERNANCE_AND_ETHICS.pdf.json"}
                ],
            },
            "Semester 4":{
               "CORPORATE ACCOUNTING II": [
                    {"title": "Corporate Accounting", "file": "No_images_dataBCOMGEN/Corporate-Accounting 2.pdf.json"}
                 ], 
            }
            
        },
        "3rd Year": {
            "Semester 5": {
                "Auditing": [
                    {"title": "Auditing and Assurance", "file": "No_images_dataBCOMGEN/Auditing and assurance explains the concepts, principles and techniques of auditing (Basu, Sanjib Kumar) (Z-Library) (1).pdf.json"}
                ],
                "Cost Accounting":[
                    {"title": "Cost Accounting Part 1 of 2", "file": "No_images_dataBCOMGEN/Cost Accounting Part 1 of 2.pdf.json"},
                    {"title": "Cost Accounting Part 2 of 2", "file": "No_images_dataBCOMGEN/Cost Accounting Part 2 of 2.pdf.json"},
                ],
                "Income Tax":[
                     {"title": "Income-tax-book", "file": "No_images_dataBCOMGEN/Income-tax-book.pdf.json"},
                ]
            },
            "Semester 6": { 
                "Income Tax":[
                     {"title": "Income-tax-book", "file": "No_images_dataBCOMGEN/Income-tax-book.pdf.json"},
                ]
            }
        }
    },
    "Bachelor of Business Administration": {
        "1st Year": {
            "Semester 1": {
                "Marketing Management": [
                    {"title": "Marketing Management (Kotler)", "file": "No_images_dataBBA/Marketing-Management-text-book-1.pdf.json"},
                    {"title": "Principles of Marketing (Armstrong)", "file": "No_images_dataBBA/Principles of Marketing -.pdf.json"},
                    {"title": "Principles of Marketing (Mumbai Univ)", "file": "No_images_dataBBA/Principles-of-Marketing-University of Mumbai.pdf.json"}
                ]
            },
            "Semester 2": {
                "Management Process": [
                    {"title": "Fundamentals of Business Process Mgmt", "file": "No_images_dataBBA/Fundamentals_of_Business_Process_Management_1.pdf.json"},
                    {"title": "Management Process & OB", "file": "No_images_dataBBA/Management Process & Organisational Behaviour- Sidharta LMS.pdf.json"},
                    {"title": "Management Concepts", "file": "No_images_dataBBA/Management-Concepts-Practices.pdf.json"},
                    {"title": "Management Theory", "file": "No_images_dataBBA/Managment Theory and Practice - Calicut University.pdf.json"}
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                 "Production and Materials Management": [
                    {"title": "Materials Management", "file": "No_images_dataBBA/Materials Management - Emgywomenscollege.pdf.json"},
                    {"title": "Production and Operations Mgmt", "file": "No_images_dataBBA/Production and Operations Management Systems.pdf.json"},
                    {"title": "Production and Materials Management", "file": "No_images_dataBBA/Production and Materials Management- Pondichery university.pdf.json"}
                 ],
                 "Accounting For Management - I": [
                    {"title": "Financial Accounting (Dr.NisikantJha)", "file": "No_images_dataBBA/Finance and Accounting uk.pdf.json"},
                    {"title": "Financial Accounting (Annand)", "file": "No_images_dataBBA/Introduction_to_Financial_Accounting_Second_Edition_22913.pdf.json"},
                    {"title": "IFRS Fundamentals", "file": "No_images_dataBBA/IFRS by tp gosh.pdf.json"},
                    {"title": "Management Accounting", "file": "No_images_dataBBA/Management Accounting - Pondichery University.pdf.json"},
                    {"title": "Financial Accounting (BMS)", "file": "No_images_dataBBA/Financial Accounting - BMS .pdf.json"}
                 ]
            },
            "Semester 4": {
                "Logistics and Supply Chain Management": [
                    {"title": "Logistics and SCM (LPU)", "file": "No_images_dataBBA/LOGISTICS_AND_SUPPLY_CHAIN_MANAGEMENT - Lovely Professional University.pdf.json"},
                    {"title": "Logistics and SCM (Christopher)", "file": "No_images_dataBBA/Logistics and Supply Chain Management- 5th edition.pdf.json"},
                    {"title": "SCM and Logistics (Himachal)", "file": "No_images_dataBBA/supply chain management and logistics - Himachal university.pdf.json"}
                ],
                "Accounting For Management - II": [
                    {"title": "Cost and Management Accounting", "file": "No_images_dataBBA/Cost and Management Accounting.pdf.json"},
                    {"title": "Cost Accounting II", "file": "No_images_dataBBA/Cost Accounting -II.pdf.json"},
                    {"title": "Cost Management", "file": "No_images_dataBBA/Cost-Management.pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "Entrepreneurship and Project Management": [
                    {"title": "Entrepreneurship Development", "file": "No_images_dataBBA/Entrepreneurship Development - Vedanta.pdf.json"},
                    {"title": "ED and Project Mgmt", "file": "No_images_dataBBA/Entrepreneurship Development and Project Management- Himachal University.pdf.json"},
                    {"title": "Project Management (HKU)", "file": "No_images_dataBBA/Project_Management- Hong Kong University.pdf.json"},
                    {"title": "Project Management (Kerzner)", "file": "No_images_dataBBA/project-management-harold-kerzner1.pdf.json"}
                ],
                "Strategic Management": [
                    {"title": "Strategic Management (Thompson)", "file": "No_images_dataBBA/Strategic Management -Awareness and Change.pdf.json"},
                    {"title": "Strategic Management (David)", "file": "No_images_dataBBA/Strategic management- Concept & Cases.pdf.json"},
                    {"title": "Strategic Management (Kennedy)", "file": "No_images_dataBBA/Strategic-Management- REED.pdf.json"}
                ],
                "Capital Markets & Investment Management": [
                    {"title": "Investment Analysis", "file": "No_images_dataBBA/Investment Analysis and Portfolio Management_TYBMS V 2016-17.pdf.json"},
                    {"title": "Indian Financial System", "file": "No_images_dataBBA/Indian Financial Systmem -Calicult University.pdf.json"},
                    {"title": "Capital Markets Law", "file": "No_images_dataBBA/CapitalMarketandSecuritesLaw.pdf.json"}
                ],
                "Business Research Methods": [
                    {"title": "Business Research Methods (Cooper)", "file": "No_images_dataBBA/Business Research Methods - David R Cooper.pdf.json"},
                    {"title": "Research Methodology (IIMM)", "file": "No_images_dataBBA/Research Methodology - IIMM.pdf.json"},
                    {"title": "Research Methodology (Kothari)", "file": "No_images_dataBBA/Research Methodology - CR Kothari.pdf.json"},
                    {"title": "Generative AI", "file": "No_images_dataBBA/generative-ai-harvard.pdf.json"},
                    {"title": "Big Data Analytics", "file": "No_images_dataBBA/Big Data Analytics.pdf.json"}
                ],
            },
            "Semester 6":{
                 "Business Communications and Managerial Skills":[
                    {"title":"Business Communication ", "file": "No_images_dataBBA/Business Communication-ITS GHAZIABHAD.pdf.json"},
                    {"title": "Business Communication ", "file": "No_images_dataBBA/Business-Communication-peter hartely.pdf.json"},
                    {"title": "Managerial Skill Development ", "file": "No_images_dataBBA/Managerial-Skill-Development-cv raman university.pdf.json"},
                ],
                "Business Finance":[
                    {"title": "Financial Management Theory & Practice", "file": "No_images_dataBBA/Financial Management -Theory & Practice.pdf.json"},
                    {"title": "Financial Management Text,Problems & Cases", "file": "No_images_dataBBA/financial mangement k.pdf.json"},
                    {"title": "Financial Management", "file": "No_images_dataBBA/Financial-Management-EIILM.pdf.json"},
                ],
                "Business Taxation":[
                     {"title": "Direct Taxation", "file": "No_images_dataBBA/Direct Taxation.pdf.json"},
                     {"title": "Indirect Tax & Customs Law", "file": "No_images_dataBBA/Indirect Taxation & Customs Law.pdf.json"},
                     {"title": "Income Tax Act 1961 -Bare Act", "file": "No_images_dataBBA/Income Tax Act 1961-Bare Act.pdf.json"},
                ]
            }
        }
    },
    "Bachelor of Commerce (Computer Applications)": {
        "1st Year": {
            "Semester 1": {
                "Computer Application in E-commerce": [
                    {"title": "E - Commerce", "file": "No_images_dataBCOMCA/E Commerce.pdf.json"},
                    
                ],
                "Essentails of Business Economy":[
                    {"title": "business eco", "file": "No_images_dataBCOMCA/business Eco.pdf.json"}
                ],
                "Financial Accounting and Accounting Standard":[
                    {"title": "Financial Accounting and Accounting Standard", "file": "No_images_dataBCOMCA/Financial Accounting and Accounting Standard .pdf.json"}
                ]
            },
            "Semester 2": {
                "Corporate Accounting And Audting": [
                    {"title": "Corporate Accounting and Auditing", "file": "No_images_dataBCOMCA/Corporate Accounting and Auditing.pdf.json"}
                ],
                "Office Automation Package": [
                    {"title": "Office Automation Package", "file": "No_images_dataBCOMCA/OfficeAutomationPackage.pdf.json"}
                ],
                "Modern Business Cpmmunication":[
                    {"title": "Business Communication ", "file": "No_images_dataBCOMCA/Business Comunication.pdf.json"}
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                "Modern Management Techniques": [
                     {"title": "5S for Services", "file": "No_images_dataBCOMCA/5S_Principle.pdf.json"},
                     {"title": "5S Guide", "file": "No_images_dataBCOMCA/Guide-5SP_12.28.17.pdf.json"},
                     {"title": "BPO", "file": "No_images_dataBCOMCA/Business Process Outsourcing (BPO).pdf.json"},
                     {"title": "Outsourcing", "file": "No_images_dataBCOMCA/The Outsourcing.pdf.json"},
                     {"title": "Poka Yoke", "file": "No_images_dataBCOMCA/Poka_yoke_B.pdf.json"},
                     {"title": "Toyota Kaizen", "file": "No_images_dataBCOMCA/Toyota Kaizen Methods _ Six Steps to Improvement. ( PDFDrive ).pdf.json"},
                     {"title": "Quality Mgmt & ISO 9001", "file": "No_images_dataBCOMCA/QUALITY MANAGEMENT &  ISO 9001 STANDARD.pdf.json"},
                     {"title": "Zero Defect Zero Effect", "file": "No_images_dataBCOMCA/ZERO DEFECT ZERO EFFECT Scheme.pdf.json"},
                     {"title": "Waste Reduction Toolkit", "file": "No_images_dataBCOMCA/Waste Reduction Project Toolkit 2017.pdf.json"},
                     {"title": "Solid Waste Management", "file": "No_images_dataBCOMCA/Solid_waste_management_UNEP_2005.pdf.json"},
                     {"title": "Sustainability Waste Booklet", "file": "No_images_dataBCOMCA/Sustainability-Waste-booklet_web.pdf.json"},
                     {"title": "UnderStanding Stress", "file": "No_images_dataBCOMCA/Understanding Stress.pdf.json"},
                     {"title": "Stress Management Skill", "file": "No_images_dataBCOMCA/Stress-Management-Skill.pdf.json"},
                     {"title": "Stress Management", "file": "No_images_dataBCOMCA/The_Stress_Management.pdf.json"},
                     {"title": "Six Sigma", "file": "No_images_dataBCOMCA/Six Sigma.pdf.json"},    
                ],
                "Quantitative Applications for Business-1": [
                    {"title": "Reasoning (RS Agarwal)", "file": "No_images_dataBCOMCA/A Modern Approach to Verbal and Non Verbal Reasoning-R S Agarwal.pdf.json"},
                    {"title": "Statistics Content", "file": "No_images_dataBCOMCA/Statistics-Content.pdf.json"},
                    {"title": "Modern Approach", "file": "No_images_dataBCOMCA/A Modern Approach to Verbal and Non Verbal Reasoning-R S Agarwal.pdf.json"},
                ],
                "Relational Database Management System": [
                    {"title": "RDBMS", "file": "No_images_dataBCOMCA/RELATIONAL DATABASE-MANAGEMENT SYSTEM.pdf.json"}
                ],
                "Programming in Java":[
                    {"title": "java syllabus notes", "file": "No_images_dataBCOMCA/Java syllabus notes.pdf.json"}
                ]
            },
            "Semester 4": {
                "Data Analytics with R Programming": [
                    {"title": "R Programming", "file": "No_images_dataBCOMCA/R Programming.pdf.json"}
                ],
                "Business Finance": [
                     {"title": "Indian Financial System", "file": "No_images_dataBCOMCA/Indian Financial System.pdf.json"},
                     {"title": "Time Value of Money (Ex)", "file": "No_images_dataBCOMCA/1. Time Value of Money-Excercises.pdf.json"},
                     {"title": "Capital Structure (Ex)", "file": "No_images_dataBCOMCA/2 Capital Structure.Excercise.pdf.json"},
                     {"title": "Capital Budgeting (Ex)", "file": "No_images_dataBCOMCA/3. Capital Budgeting.Exercise.pdf.json"}
                ],
                "Legal Application in Business": [
                    {"title": "LAIB 1.1", "file": "No_images_dataBCOMCA/LAIB - 1.1.pdf.json"},
                    {"title": "LAIB 1.2", "file": "No_images_dataBCOMCA/LAIB - 1.2.pdf.json"},
                    {"title": "LAIB 2.1", "file": "No_images_dataBCOMCA/LAIB - 2.1.pdf.json"},
                    {"title": "LAIB 2.2", "file": "No_images_dataBCOMCA/LAIB - 2.2.pdf.json"},
                    {"title": "LAIB 2.3", "file": "No_images_dataBCOMCA/LAIB - 2.3.pdf.json"},
                    {"title": "LAIB 2.4", "file": "No_images_dataBCOMCA/LAIB - 2.4.pdf.json"},
                    {"title": "LAIB 2.5", "file": "No_images_dataBCOMCA/LAIB - 2.5.pdf.json"},
                    {"title": "LAIB 3.1", "file": "No_images_dataBCOMCA/LAIB - 3.1.pdf.json"},
                    {"title": "LAIB 3.2", "file": "No_images_dataBCOMCA/LAIB - 3.2.pdf.json"},
                    {"title": "LAIB 4.1", "file": "No_images_dataBCOMCA/LAIB - 4.1.pdf.json"},
                    {"title": "LAIB 4.2", "file": "No_images_dataBCOMCA/LAIB - 4.2.pdf.json"},
                    {"title": "LAIB 4.3", "file": "No_images_dataBCOMCA/LAIB - 4.3.pdf.json"},
                    {"title": "LAIB 5.1", "file": "No_images_dataBCOMCA/LAIB - 5.1.pdf.json"},
                    {"title": "LAIB 5.2", "file": "No_images_dataBCOMCA/LAIB - 5.2.pdf.json"}
                ],
                "Quantitative Applications for Business- II": [
                    {"title": "Quantitative Techniques II", "file": "No_images_dataBCOMCA/QUANTITATIVE_TECHNIQUES_II.pdf.json"},
                    {"title": "Statistical Methods", "file": "No_images_dataBCOMCA/STATISTICAL METHODS.pdf.json"},
                    {"title": "Reasoning E-Book", "file": "No_images_dataBCOMCA/Reasoning E-Book.pdf.json"}
                ],
                "Software Development with Visual Basic": [
                    {"title": "Visual Basic", "file": "No_images_dataBCOMCA/Visual Basic in easy steps_ Covers Visual Basic 2015 ( PDFDrive ).pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "Internet in Web Technology": [
                    {"title": "Internet Web Tech", "file": "No_images_dataBCOMCA/Internet-Web-Technology_SM.pdf.json"},
                    {"title": "Web Technology", "file": "No_images_dataBCOMCA/WebTechnology.pdf.json"}
                ],
                "Problem Solving using Python": [
                     {"title": "Problem Solving and Python", "file": "No_images_dataBCOMCA/Problem-Solving-and-Python.pdf.json"},
                     {"title": "Python Programming Notes", "file": "No_images_dataBCOMCA/PYTHON PROGRAMMING NOTES.pdf.json"},
                     {"title": "Programming in Python", "file": "No_images_dataBCOMCA/Programming in python.pdf.json"}
                ],
                "Marketing Research for Business": [
                    {"title": "Research Methodology (Kothari)", "file": "No_images_dataBCOMCA/Research Methodology - C.R.Kothari.pdf.json"}
                ],
                "Recent Trends in Human Resource Management": [
                    {"title": "Knowledge Management Essentials", "file": "No_images_dataBCOMCA/Essentials of Knowledge Management.pdf.json"},
                    {"title": "Human Capital Management", "file": "No_images_dataBCOMCA/HUMAN CAPITAL MANAGEMENT.pdf.json"},
                    {"title": "Human Resource Book", "file": "No_images_dataBCOMCA/Human-Resource-Book.pdf.json"},
                    {"title": "Intro to HRM", "file": "No_images_dataBCOMCA/An Introduction to Human Resource Management- 2nd edition.pdf.json"},
                    {"title": "CSR", "file": "No_images_dataBCOMCA/Corporate Social Responsibility.pdf.json"},
                    {"title": "Thoughts of Power", "file": "No_images_dataBCOMCA/Thoughts-of-Power-by-Swami-Vivekananda.pdf.json"},
                    {"title": "Business Ethics", "file": "No_images_dataBCOMCA/Business-Ethics-2.pdf.json"},
                    {"title": "Intro to Stress Management", "file": "No_images_dataBCOMCA/Introducation to Stress Management.pdf.json"},
                    {"title": "Stress Management", "file": "No_images_dataBCOMCA/The_Stress_Management.pdf.json"},
                    {"title": "Stress Management Skill", "file": "No_images_dataBCOMCA/Stress-Management-Skill.pdf.json"},
                    {"title": "Understanding Stress", "file": "No_images_dataBCOMCA/Understanding Stress.pdf.json"}
                ],
                "Taxation and its Application": [
                    {"title": "Income Tax AY 2025-26", "file": "No_images_dataBCOMCA/Income Tax A.Y 2025-26.pdf.json"},
                    {"title": "Indirect Tax", "file": "No_images_dataBCOMCA/Indirect Tax.pdf.json"}
                ]
            },
            "Semester 6": {
                "Computerized Accounting Application": [
                    {"title": "Tally ERP 9 Notes", "file": "No_images_dataBCOMCA/Tally-ERP-9-Full-Notes.pdf.json"}
                ],
                "Blockchain Technology in Cryptocurrency": [
                    {"title": "Cryptocurrencies and Blockchain", "file": "No_images_dataBCOMCA/Cryptocurrencies-and-blockchain.pdf.json"}
                ],
                 "Entrepreneurial Development": [
                    {"title": "Entrepreneurship Manual", "file": "No_images_dataBCOMCA/Manual on Entrepreurship development.pdf.json"}
                ],
                "Banking and financial Service":[
                    {"title":"INDIAN FINANCIAL SYSTEM","file": "No_images_dataBCOMCA/Indian Financial System.pdf.json"}
                ],
                "Goods & Service Tax ":[
                    {"title":"Indirect tax","file": "No_images_dataBCOMCA/Indirect Tax.pdf.json"}
                ]
            }
        }
    },
    "Bachelor of Computer Applications": {
        "1st Year": {
            "Semester 1": {
                "C Programming (T+P)": [
                    {"title": "Let Us C 19th Edition", "file": "No_images_dataBCA/Let us C _ Yashwant Kanetkar.pdf.json"},
                    {"title": "Programming in ANSI C", "file": "No_images_dataBCA/PROGRAMMING IN C - Dr.E.BALAGURUSAMY.pdf.json"},
                    {"title": "Logic and Computer Design Fundamentals", "file": "No_images_dataBCA/Logic_and_Computer_Design_Fundamentals_-_4th_International_Edition.pdf.json"}
                ],
                "Operating Systems (T+P)": [
                    {"title": "Operating system concepts", "file": "No_images_dataBCA/Silberschatz 9th edition.pdf.json"},
                    {"title": "Unix-Shell-Programming", "file": "No_images_dataBCA/unix-shell-programming.pdf.json"},
                    {"title": "UnixProgrammingEnvironment", "file": "No_images_dataBCA/UNIXProgrammingEnvironment.pdf.json"},
                    {"title": "PG Trb Tamil", "file": "No_images_dataBCA/PG Trb Tamil.pdf.json"},
                ]
            },
            "Semester 2": {
                "Data Structures and Algorithms (T+P)": [
                    {"title": "Data Structures Using C++", "file": "No_images_dataBCA/DATA STRUCTURE FINAL.pdf.json"},
                    {"title": "OOPS C++", "file": "No_images_dataBCA/OOPS C++.pdf.json"},
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                "Java Programming(T+P)": [
                    {"title": "Beginning JavaScript with DOM Scripting and Ajax", "file": "No_images_dataBCA/Beginning JavaScript with DOM Scripting & Ajax.pdf.json"},
                    {"title": "Java A Learner’s Guide to Real-World Programming", "file": "No_images_dataBCA/Head_First_Java_A_Brain-Friendly_Guide.pdf.json"},
                    {"title": "JavaScript from Beginner to Professional", "file": "No_images_dataBCA/Svekis L. JavaScript from Beginner to Professional 2021.pdf.json"},
                    {"title": "JavaTM The Complete Reference", "file": "No_images_dataBCA/The Complete Reference -Java.pdf.json"},
                    {"title": "Java", "file": "No_images_dataBCA/JAVA.pdf.json"},
                    {"title": "Java1", "file": "No_images_dataBCA/JAVA1.pdf.json"},
                ],
                "Relational Database Management System (T+ P)": [
                    {"title": "Database System Concepts", "file": "No_images_dataBCA/Database System Concepts 6th edition.pdf.json"},
                    {"title": "Oracle PL/SQL by Example", "file": "No_images_dataBCA/Oracle PL SQL by Example.pdf.json"}
                ],
                "Digital Image Processing": [
                    {"title": "Digital Image Processing (3rd Edition)", "file": "No_images_dataBCA/Digital.Image.Processing.3rd.Edition.www.EBooksWorld.ir.pdf.json"},
                    {"title": "Digital Image Processing (4th Edition)", "file": "No_images_dataBCA/Gonzales,Woods-Digital.Image.Processing.4th.Edition.pdf.json"}
                ],
                "Computer Networks and Cyber Security": [
                    {"title": "Computer Networks", "file": "No_images_dataBCA/Computer Network Andrew S. Tanenbaum - Computer Networks.pdf.json"}
                ]
            },
            "Semester 4": {
                "Distributed Databaase Management Systems": [
                    {"title": "Distributed Databaases Principles and Systems", "file": "No_images_dataBCA/DDBMS (Only Scan Page NO 551-607) .pdf.json"},

                ],
                "Advanced Java": [
                    {"title": "Head First Servlets and JSP", "file": "No_images_dataBCA/Head First Servlets and JSP, Second Edition.pdf.json"}
                ],
                "Java Full Stack": [
                    {"title": "Unit 1", "file": "No_images_dataBCA/UNIT 1 - JAVA FULL STACK.pdf.json"},
                    {"title": "Unit 2", "file": "No_images_dataBCA/Unit 2 JAVA FULL STACK.pdf.json"},
                    {"title": "Unit 3 & 4", "file": "No_images_dataBCA/UNIT III AND UNI IV FULL STACK.pdf.json"},
                    {"title": "Unit 5", "file": "No_images_dataBCA/UNIT V JAVA FULL STACK.pdf.json"}
                ],
                "Cloud Computing": [
                    {"title": "Cloud Computing", "file": "No_images_dataBCA/Cloud Computing.pdf.json"}
                ],
                "Web Technology": [
                    {"title": "Web Technology", "file": "No_images_dataBCA/WEB TECHNOLOGY.pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "PHP Programming (T+P)": [
                    {"title": "PHP and MySQL Web Development", "file": "No_images_dataBCA/PHP and MySQL Web Development, Luke Welling and Laura Thomson, Fifth Edition.pdf.json"}
                ],
                "Mobile Applications Development (T+P)": [
                    {"title": "Android Application Development For Dummies", "file": "No_images_dataBCA/android-application-development-for-for-dummies.pdf.json"},
                    {"title": "Professional Android Application Development", "file": "No_images_dataBCA/Professional_Android_Application_Development.pdf.json"},
                    {"title": "Text Book for Android", "file": "No_images_dataBCA/Text Book for Android.pdf.json"}
                ],
                "Data Mining and Data Warehousing (E1)": [
                    {"title": "Data Mining", "file": "No_images_dataBCA/Data Mining The Textbook.pdf.json"},
                    {"title": "Data Mining Concepts and Techniques", "file": "No_images_dataBCA/Han - Data Mining Concepts and Techniques 3rd Edition - 2012.pdf.json"},
                    {"title": "Web Data Mining", "file": "No_images_dataBCA/Web_Data_Mining__2nd_Edition__Exploring_Hyperlinks__Contents__and_Usage_Data (1).pdf.json"}
                ],
                "Software Engineering (E2)": [
                    {"title": "Software Engineering", "file": "No_images_dataBCA/Software Engineering_Roger S. Pressman.pdf.json"}
                ]
            },
            "Semester 6": {
                "Big Data Analytics": [
                    {"title": "Big Data Analytics", "file": "No_images_dataBCA/BIG DATA ANALYSTICS.pdf.json"},
                    {"title": "Big Data Analytics Book 2", "file": "No_images_dataBCA/BIG DATA ANALYSTICS BOOK 2 .pdf.json"},
                    {"title": "Intelligent Data Analytics", "file": "No_images_dataBCA/BIG DATA (SCAN PAGE 69- 264).pdf.json"}
                ],
                "R Programming (T+P)": [
                    {"title": "R Programming", "file": "No_images_dataBCA/R Programming.pdf.json"},
                    {"title": "R in Action", "file": "processed_data/R Programming.pdf.json"}
                ],
                "Deep Learning": [
                    {"title": "Deep Learning", "file": "No_images_dataBCA/deeplearningbook.pdf.json"}
                ],
                "Python":[
                     {"title": "Python DataScience", "file": "No_images_dataBCA/Python_Datascience.pdf.json"},
                     {"title": "Python 1", "file": "No_images_dataBCA/Python1.pdf.json"},
                ],
                 "IOT":[
                    { "title": "IOT", "file": "No_images_dataBCA/IoT.pdf.json"}    
                ],
                "GEN AI":[
                  { "title": "GEN AI", "file": "No_images_dataBCA/GEN AI.pdf.json"}   
                ]
            }
        }
    },
    # "Bachelor of Computer Science": {
    #     "1st Year": {
    #         "Semester 1": {
    #             "C Programming (T+P)": [
    #                 {"title": "Let Us C 19th Edition", "file": "processed_data/Let us C _ Yashwant Kanetkar.pdf.json"}
    #             ],
    #             # "Operating Systems (T+P)": [
    #             #     {"title": "Operating System Concepts", "file": "Operating_System_Concepts.pdf.json"},
    #             #     {"title": "Unix Shell Programming", "file": "Unix_Shell_Programming.pdf.json"},
    #             #     {"title": "The Unix Programming Environment", "file": "The_Unix_Programming_Environment.pdf.json"}
    #             # ]
    #         },
    #         "Semester 2": {
    #             "Object Oriented Programming (T+P)": [
    #                 {"title": "Object Oriented Programming With C++", "file": "Object_Oriented_Programming_With_CPP.pdf.json"}
    #             ],
    #             "Data Structures and Algorithms (T+P)": [
    #                 {"title": "Data Structures Using C++", "file": "No_images_data/DATA STRUCTURE FINAL.pdf.json"}
    #             ]
    #         }
    #     },
    #     "2nd Year": {
    #         "Semester 3": {
    #             "Java Programming (T+P)": [
    #                 {"title": "Beginning JavaScript with DOM Scripting and Ajax", "file": "No_images_data/Beginning JavaScript with DOM Scripting & Ajax.pdf.json"},
    #                 {"title": "Java A Learner’s Guide to Real-World Programming", "file": "Java_A_Learners_Guide.pdf.json"},
    #                 {"title": "JavaScript from Beginner to Professional", "file": "No_images_data/Svekis L. JavaScript from Beginner to Professional 2021.pdf.json"},
    #                 {"title": "Java The Complete Reference", "file": "The Complete Reference -Java.pdf.json"}
    #             ],
    #             "Relational Database Management System (T+P)": [
    #                 {"title": "Database System Concepts", "file": "No_images_data/Database System Concepts 6th edition.pdf.json"},
    #                 {"title": "Oracle PL/SQL by Example", "file": "No_images_data/Oracle PL SQL by Example.pdf.json"}
    #             ]
    #         },
    #         "Semester 4": {
    #             "Advanced Java": [
    #                 {"title": "Head First Servlets and JSP", "file": "No_images_data/Head First Servlets and JSP, Second Edition.pdf.json"}
    #             ],
    #             # "Java Full Stack": [
    #             #     {"title": "Pro Angular", "file": "Pro_Angular.pdf.json"},
    #             #     {"title": "Designing Applications with Spring Boot", "file": "Designing_Applications_with_Spring_Boot.pdf.json"},
    #             #     {"title": "Spring in Action", "file": "Spring_in_Action.pdf.json"},
    #             #     {"title": "Effective DevOps", "file": "Effective_DevOps.pdf.json"}
    #             # ],
    #             "Web Technology": [
    #                 {"title": "Beginning ASP.NET 4.5", "file": "No_images_data/WEB TECHNOLOGY.pdf.json"}
    #             ]
    #         }
    #     },
    #     "3rd Year": {
    #         "Semester 5": {
    #             "PHP Programming (T+P)": [
    #                 {"title": "PHP and MySQL Web Development", "file": "No_images_data/PHP and MySQL Web Development, Luke Welling and Laura Thomson, Fifth Edition.pdf.json"}
    #             ],
    #             "Mobile Applications Development (T+P)": [
    #                 {"title": "Android Application Development For Dummies", "file": "No_images_data/android-application-development-for-for-dummies.pdf.json"},
    #                 {"title": "Professional Android Application Development", "file": "No_images_data/Professional_Android_Application_Development.pdf.json"},

    #             ],
    #             "Computer Networks and Cyber Security": [
    #                 {"title": "Computer Networks", "file": "No_images_data/Computer Network Andrew S. Tanenbaum - Computer Networks.pdf.json"}
    #             ],
    #             "Data Mining and Data Warehousing (E1)": [
    #                 {"title": "Data Mining", "file": "No_images_data/Data Mining The Textbook.pdf.json"},
    #                 {"title": "Data Mining Concepts and Techniques", "file": "No_images_data/Han - Data Mining Concepts and Techniques 3rd Edition - 2012.pdf.json"},
    #                 {"title": "Web Data Mining", "file": "No_images_data/Web_Data_Mining__2nd_Edition__Exploring_Hyperlinks__Contents__and_Usage_Data (1).pdf.json"}
    #             ],
    #             "Software Engineering (E2)": [
    #                 {"title": "Software Engineering A Practitioner's Approach", "file": "No_images_data/Software Engineering_Roger S. Pressman.pdf.json"}
    #             ]
    #         },
    #         "Semester 6": {
    #             # "Python Programming (T+P)": [
    #             #     {"title": "Python Programming Using Problem Solving Approach", "file": "Python_Programming_Using_Problem_Solving_Approach.pdf.json"}
    #             # ],
    #             "Internet of Things (IoT)": [
    #                 {"title": "Internet of Things", "file": "processed_data/IoT.pdf.json"}
    #             ],
    #             "Big Data Analytics": [
    #                 # {"title": "Intelligent Data Analytics", "file": "Intelligent_Data_Analytics.pdf.json"},
    #                 {"title": "Introduction to Big Data", "file": "processed_data/BIG DATA (SCAN PAGE 69- 264).pdf.json"},
    #                 {"title": "Big Data Analytics", "file": "processed_data/BIG DATA ANALYSTICS.pdf.json"}
    #             ],
    #             "Cloud Computing": [
    #                 {"title": "Cloud Computing using the Windows Azure Platform", "file": "processed_data/Cloud Computing.pdf.json"}
    #             ],
    #             "R Programming (T+P)": [
    #                 {"title": "R in Action", "file": "processed_data/R Programming.pdf.json"}
    #             ],
    #             "Deep Learning": [
    #                 {"title": "Deep Learning", "file": "processed_data/deeplearningbook.pdf.json"}
    #             ]
    #         }
    #     }
    # },

     "Bachelor of Computer Science": {
        "1st Year": {
            "Semester 1": {
                "C Programming (T+P)": [
                    {"title": "Let Us C 19th Edition", "file": "No_images_dataBCA/Let us C _ Yashwant Kanetkar.pdf.json"},
                    {"title": "Programming in ANSI C", "file": "No_images_dataBCA/PROGRAMMING IN C - Dr.E.BALAGURUSAMY.pdf.json"},
                    {"title": "Logic and Computer Design Fundamentals", "file": "No_images_dataBCA/Logic_and_Computer_Design_Fundamentals_-_4th_International_Edition.pdf.json"}
                ],
                "Operating Systems (T+P)": [
                    {"title": "Operating system concepts", "file": "No_images_dataBCA/Silberschatz 9th edition.pdf.json"},
                    {"title": "Unix-Shell-Programming", "file": "No_images_dataBCA/unix-shell-programming.pdf.json"},
                    {"title": "UnixProgrammingEnvironment", "file": "No_images_dataBCA/UNIXProgrammingEnvironment.pdf.json"},
                     
                ]
            },
            "Semester 2": {
                "Data Structures and Algorithms (T+P)": [
                    {"title": "Data Structures Using C++", "file": "No_images_dataBCA/DATA STRUCTURE FINAL.pdf.json"},
                    {"title": "OOPS C++", "file": "No_images_dataBCA/OOPS C++.pdf.json"},
                ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                "Java Programming(T+P)": [
                    {"title": "Beginning JavaScript with DOM Scripting and Ajax", "file": "No_images_dataBCA/Beginning JavaScript with DOM Scripting & Ajax.pdf.json"},
                    {"title": "Java A Learner’s Guide to Real-World Programming", "file": "No_images_dataBCA/Head_First_Java_A_Brain-Friendly_Guide.pdf.json"},
                    {"title": "JavaScript from Beginner to Professional", "file": "No_images_dataBCA/Svekis L. JavaScript from Beginner to Professional 2021.pdf.json"},
                    {"title": "JavaTM The Complete Reference", "file": "No_images_dataBCA/The Complete Reference -Java.pdf.json"},
                    {"title": "Java", "file": "No_images_dataBCA/JAVA.pdf.json"},
                    {"title": "Java1", "file": "No_images_dataBCA/JAVA1.pdf.json"},
                ],
                "Relational Database Management System (T+ P)": [
                    {"title": "Database System Concepts", "file": "No_images_dataBCA/Database System Concepts 6th edition.pdf.json"},
                    {"title": "Oracle PL/SQL by Example", "file": "No_images_dataBCA/Oracle PL SQL by Example.pdf.json"}
                ],
            },
            "Semester 4": {
                "Distributed Databaase Management Systems": [
                    {"title": "Distributed Databaases Principles and Systems", "file": "No_images_dataBCA/DDBMS (Only Scan Page NO 551-607) .pdf.json"}
                ],
                "Advanced Java": [
                    {"title": "Head First Servlets and JSP", "file": "No_images_dataBCA/Head First Servlets and JSP, Second Edition.pdf.json"}
                ],
                "Java Full Stack": [
                    {"title": "Unit 1", "file": "No_images_dataBCA/UNIT 1 - JAVA FULL STACK.pdf.json"},
                    {"title": "Unit 2", "file": "No_images_dataBCA/Unit 2 JAVA FULL STACK.pdf.json"},
                    {"title": "Unit 3 & 4", "file": "No_images_dataBCA/UNIT III AND UNI IV FULL STACK.pdf.json"},
                    {"title": "Unit 5", "file": "No_images_dataBCA/UNIT V JAVA FULL STACK.pdf.json"}
                ],
                "Cloud Computing": [
                    {"title": "Cloud Computing", "file": "No_images_dataBCA/Cloud Computing.pdf.json"}
                ],
                "Web Technology": [
                    {"title": "Web Technology", "file": "No_images_dataBCA/WEB TECHNOLOGY.pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "PHP Programming (T+P)": [
                    {"title": "PHP and MySQL Web Development", "file": "No_images_dataBCA/PHP and MySQL Web Development, Luke Welling and Laura Thomson, Fifth Edition.pdf.json"}
                ],
                "Mobile Applications Development (T+P)": [
                    {"title": "Android Application Development For Dummies", "file": "No_images_dataBCA/android-application-development-for-for-dummies.pdf.json"},
                    {"title": "Professional Android Application Development", "file": "No_images_dataBCA/Professional_Android_Application_Development.pdf.json"},
                    {"title": "Text Book for Android", "file": "No_images_dataBCA/Text Book for Android.pdf.json"}
                ],
                "Data Mining and Data Warehousing (E1)": [
                    {"title": "Data Mining", "file": "No_images_dataBCA/Data Mining The Textbook.pdf.json"},
                    {"title": "Data Mining Concepts and Techniques", "file": "No_images_dataBCA/Han - Data Mining Concepts and Techniques 3rd Edition - 2012.pdf.json"},
                    {"title": "Web Data Mining", "file": "No_images_dataBCA/Web_Data_Mining__2nd_Edition__Exploring_Hyperlinks__Contents__and_Usage_Data (1).pdf.json"}
                ],
                "Software Engineering (E2)": [
                    {"title": "Software Engineering", "file": "No_images_dataBCA/Software Engineering_Roger S. Pressman.pdf.json"}
                ]
            },
            "Semester 6": {
                "Big Data Analytics": [
                    {"title": "Big Data Analytics", "file": "No_images_dataBCA/BIG DATA ANALYSTICS.pdf.json"},
                    {"title": "Big Data Analytics Book 2", "file": "No_images_dataBCA/BIG DATA ANALYSTICS BOOK 2 .pdf.json"},
                    {"title": "Intelligent Data Analytics", "file": "No_images_dataBCA/BIG DATA (SCAN PAGE 69- 264).pdf.json"}
                ],
                "R Programming (T+P)": [
                    {"title": "R Programming", "file": "No_images_dataBCA/R Programming.pdf.json"},
                    {"title": "R in Action", "file": "processed_data/R Programming.pdf.json"}
                ],
                "Deep Learning": [
                    {"title": "Deep Learning", "file": "No_images_dataBCA/deeplearningbook.pdf.json"}
                ],
                "Python":[
                     {"title": "Python DataScience", "file": "No_images_dataBCA/Python_Datascience.pdf.json"},
                     {"title": "Python 1", "file": "No_images_dataBCA/Python1.pdf.json"},
                ],
                "IOT":[
                    { "title": "IOT", "file": "No_images_dataBCA/IoT.pdf.json"}    
                ]
            }
        }
    },
    
    "Bachelor of Commerce (Banking Management)": {
        "1st Year": {
            "Semester 1": {
                "Principles of Financial Accounting": [
                    {"title": "Financial Accounting (ICAI)", "file": "No_images_dataBCOMBM/Financial Accounting ICAI.pdf.json"},
                    {"title": "Financial Accounting", "file": "No_images_dataBCOMBM/Financial Accounting.pdf.json"},
                    {"title": "Financial Accounting (BMS)", "file": "No_images_dataBCOMBM/Financial Accounting - BMS .pdf.json"}
                ],
                "Business Management": [
                    {"title": "Principles and Practices of Management (LPU)", "file": "No_images_dataBCOMBM/DCOM102_DMGT101_PRINCIPLES_AND_PRACTICES_OF_MANAGEMENT.pdf.json"},
                    {"title": "Principles of Business Management", "file": "No_images_dataBCOMAF/e.book_Principles of Management.pdf.json"},
                    {"title": "Principles of Management(P C TRIPATHI, P N REDDY)", "file": "No_images_dataBCOMAF/Principles of management (P C Tripathi, P N Reddy) (Z-Library).pdf.json"},
                    {"title": "Principles of Management", "file": "No_images_dataBCOMAF/Principle-Of-Management.pdf.json"},
                ],
                "Business Statistics & Operations": [
                    {"title": "Business Mathematics and Statistics (Das)", "file": "No_images_dataBCOMBM/Business Mathematics and Statistics (N Das Dr. J K Das) (Z-Library).pdf.json"},
                    {"title": "Business Mathematics (ICAI)", "file": "No_images_dataBCOMBM/BUSINESS MATHEMATICS, LOGICAL REASONING AND STATISTICS (BOARD OF STUDIES ICAI) (Z-Library).pdf.json"},
                    {"title": "Business Statistics (Alagar)", "file": "No_images_dataBCOMBM/Business Statistics (K. Alagar) (Z-Library).pdf.json"}
                ]
            },
            "Semester 2": {
                 "Advanced Financial Accounting": [
                    {"title": "Advanced Accounting (Maheshwari)", "file": "No_images_dataBCOMBM/ADVANCED ACCOUNTING_3461.pdf.json"},
                    {"title": "Advanced Financial Accounting", "file": "No_images_dataBCOMBM/Advanced Financial Accounting.pdf.json"},
                    {"title": "Advanced FA", "file": "No_images_dataBCOMBM/Advanced FA.pdf.json"}
                 ],
                 "Banking Management Theory": [
                    {"title": "Banking Theory, Law and Practice (Gordon)", "file": "No_images_dataBCOMBM/Banking Theory, Law and Practice (E. Gordon K. Natarajan) (Z-Library).pdf.json"},
                    {"title": "Management of Banking and Financial Services", "file": "No_images_dataBCOMBM/Management of Banking and Financial Services (Padmalatha Suresh, Justin Paul) (Z-Library).pdf.json"},
                    {"title": "Negotiable Instruments (Goyal)", "file": "No_images_dataBCOMBM/NEGOTIABLE INSTRUMENTS, BANKING AND INSURANCE (For LL.B. Students of various Universities of India and Civil Judicial… (B.K. GOYAL) (Z-Library).pdf.json"}
                 ],
                 "Business Arithmetic & Logical": [
                    {"title": "Business Mathematics (ICAI)", "file": "No_images_dataBCOMBM/BUSINESS MATHEMATICS, LOGICAL REASONING AND STATISTICS (BOARD OF STUDIES ICAI) (Z-Library).pdf.json"}
                 ]
            }
        },
        "2nd Year": {
            "Semester 3": {
                "Company Accounts": [
                    {"title": "Corporate Accounting (Hanif)", "file": "No_images_dataBCOMBM/Corporate Accounting (M Hanif A Mukherjee) (Z-Library).pdf.json"},
                    {"title": "AAVIN FEB", "file": "No_images_dataBCOMBM/AAVIN FEB 26.pdf.json"},
                    {"title": "Document from Arunkumar", "file": "No_images_dataBCOMBM/Document from Arunkumar Chandrasekaar.pdfpdf.json"},
                     {"title": "IVN MGT", "file": "No_images_dataBCOMBM/inv mgt measurement of return.pdf.json"},
                    {"title": "Corporate Accounting (Radhika)", "file": "No_images_dataBCOMBM/Corporate Accounting (P. Radhika Anita Raman) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (Rajasekaran)", "file": "No_images_dataBCOMBM/Corporate Accounting (V. Rajasekaran, R. Lalitha) (Z-Library).pdf.json"},
                    {"title": "Corporate Accounting (UP Univ)", "file": "No_images_dataBCOMBM/Corporate Accounting  for B. Com course of Uttar Pradesh Universities (V. Rajasekaran) (Z-Library).pdf.json"}
                ],
                "Accounting for Decision Making": [
                    {"title": "Accountancy and Financial Management-I", "file": "No_images_dataBCOMBM/Accountancy and Financial Management–I (Sanjay D. Sonawane) (Z-Library).pdf.json"},
                    {"title": "Accounting For Managers (VTU)", "file": "No_images_dataBCOMBM/Accounting For Managers (For VTU) (V. Rajasekaran) (Z-Library).pdf.json"},
                    {"title": "Financial Accounting For Management", "file": "No_images_dataBCOMBM/Financial Accounting For Management (Ramachandran And K Ramkumar) (Z-Library).pdf.json"}
                ],
                "Human Resource Management": [
                    {"title": "Organizational Behaviour (Kondalkar)", "file": "No_images_dataBCOMBM/Organizational Behaviour (V.G. Kondalkar) (Z-Library).pdf.json"},
                    {"title": "Management Organizational Behaviour", "file": "No_images_dataBCOMBM/Management  Organizational Behaviour (R. B. Rudani) (Z-Library).pdf.json"},
                    {"title": "International HRM", "file": "No_images_dataBCOMBM/International Human Resource Management A Multinational Company.. (Monir H. Tayeb) (Z-Library).pdf.json"},
                    {"title": "Intro to HRM", "file": "No_images_dataBCOMBM/An Introduction to Human Resource Management- 2nd edition.pdf.json"},
                    {"title": "Intro to HRM", "file": "No_images_dataBCOMBM/hrm.pdf.json"},
                     {"title": "Human Resource Book", "file": "No_images_dataBCOMBM/Human-Resource-Book.pdf.json"},

                ],
                "Business & Corporate Law": [
                    {"title": "Business Law", "file": "No_images_dataBCOMBM/Business Law.pdf.json"},
                    {"title": "Business Law Py", "file": "No_images_dataBCOMBM/Business Law PY Univ.pdf.json"},
                    {"title": "Business Law (ICMAI)", "file": "No_images_dataBCOMBM/Business Law icmai.pdf.json"},
                    {"title": "Company Law", "file": "No_images_dataBCOMBM/CompanyLaw_BOOK.pdf.json"},
                    {"title": "Corporate and Business Laws", "file": "No_images_dataBCOMBM/CORPORATE_AND_BUSINESS_LAWS.pdf.json"},
                    {"title": "Corporate Law (ICMAI)", "file": "No_images_dataBCOMBM/Corporate law ICMAI.pdf.json"}
                ],
                "Auditing – Theory & Applications": [
                    {"title": "Auditing and Assurance (Basu)", "file": "No_images_dataBCOMBM/Auditing and assurance explains the concepts, principles and techniques of auditing (Basu, Sanjib Kumar) (Z-Library).pdf.json"},
                    {"title": "Auditing Principles and Practices", "file": "No_images_dataBCOMBM/Auditing Principles and Practices (Ashish Kumar Sana, Swapan Sarkar etc.) (Z-Library).pdf.json"},
                    {"title": "Auditing Principles and Techniques", "file": "No_images_dataBCOMBM/Auditing Principles and Techniques (Sanjib Kumar Basu) (Z-Library).pdf.json"}
                ]
            },
            "Semester 4": {
                "Principles of Financial Management": [
                    {"title": "Fundamentals of Financial Management", "file": "No_images_dataBCOMBM/Fundamentals of Financial Management (Vyuptakesh Sharan) (Z-Library).pdf.json"},
                    {"title": "Accountancy and Financial Management - I", "file": "No_images_dataBCOMBM/Accountancy and Financial Management–I (Sanjay D. Sonawane) (Z-Library).pdf.json"},
                    {"title": "Accounting for managers", "file": "No_images_dataBCOMBM/Accounting For Managers (For VTU) (V. Rajasekaran) (Z-Library).pdf.json"},
                ],
                "Insurance Theory and Accounting": [
                    {"title": "Insurance Management", "file": "No_images_dataBCOMBM/__UG_B.Com_Computer Applications_123 41 INSURANCE MANAGEMENT_5384.pdf.json"},
                    {"title": "Insurance Law and Practice", "file": "No_images_dataBCOMBM/9.3 INSURANCE LAW AND PRACTICE.pdf.json"}
                ],
                "Banking Law": [
                     {"title": "Banking Theory, Law and Practice", "file": "No_images_dataBCOMBM/Banking Theory, Law and Practice (E. Gordon K. Natarajan) (Z-Library).pdf.json"},
                     {"title": "Management of Banking Services", "file": "No_images_dataBCOMBM/Management of Banking and Financial Services (Padmalatha Suresh, Justin Paul) (Z-Library).pdf.json"},
                     {"title": "Negotiable Instruments", "file": "No_images_dataBCOMBM/NEGOTIABLE INSTRUMENTS, BANKING AND INSURANCE (For LL.B. Students of various Universities of India and Civil Judicial… (B.K. GOYAL) (Z-Library).pdf.json"}
                ],
                "International Banking": [
                    {"title": "International Banking (SBAA)", "file": "No_images_dataBCOMBM/SBAA3015.pdf.json"},
                    {"title": "International Banking and Forex", "file": "No_images_dataBCOMBM/DEFIN566_INTERNATIONAL_BANKING_AND_FOREX_MANAGEMENT.pdf.json"},
                     {"title": "International Banking", "file": "No_images_dataBCOMBM/BBM-24.pdf.json"},
                ],
                "Monetary Economics": [
                    {"title": "Monetary Economics (Handa)", "file": "No_images_dataBCOMBM/Monetary Economics (Jagdish Handa) (Z-Library).pdf.json"},
                    {"title": "Monetary Economics", "file": "No_images_dataBCOMBM/Monetary Economics 1.pdf.json"}
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "Taxation - I": [
                    {"title": "Income Tax-I", "file": "No_images_dataBCOMBM/Income Tax-I (V. Rajesh Kumar R. K. Sreekantha) (Z-Library).pdf.json"},
                    {"title": "Students' Guide to Income Tax", "file": "No_images_dataBCOMBM/Taxmann Students Guide to Income Tax Including GST (Vinod K. Singhania, Monica Singhania) (Z-Library).pdf.json"}
                ],
                "Theory of Research Analysis": [
                     {"title": "Management Research Methodology", "file": "No_images_dataBCOMBM/Management Research Methodology Integration of Principles, Methods and Techniques ( etc.) (Z-Library).pdf.json"},
                     {"title": "Research Methodology (Kothari)", "file": "No_images_dataBCOMBM/Research Methodology - Methods and Techniques (C.R. Kothari) (Z-Library).pdf.json"},
                     {"title": "Research Methodology (Kumar)", "file": "No_images_dataBCOMBM/Research Methodology. (Kumar, Ranjit) (Z-Library).pdf.json"}
                ],
                "Banking Advances": [
                    {"title": "Indian Financial System", "file": "No_images_dataBCOMBM/Indian Financial Systmem -Calicult University.pdf.json"},
                    {"title": "Indian Financial System", "file": "No_images_dataBCOMBM/2BankingandIndianFinancialSystems.pdf.json"},
                    {"title": "Merchant Banking", "file": "No_images_dataBCOMBM/Merchant Banking And Financial Services (Madhu Vij and Swati Dhawan) (Z-Library).pdf.json"},
                    {"title": "NBFC Role", "file": "No_images_dataBCOMBM/Non-Banking Financial Companies Role in Indias Development A Way Forward (R. Kannan, K. R. Shanmugam, Saumitra Bhaduri) (Z-Library).pdf.json"}
                ],
                "Capital Markets and Financial Service": [
                    {"title": "Capital Markets Law", "file": "No_images_dataBCOMBM/CapitalMarketandSecuritesLaw.pdf.json"},
                    {"title": "Indian Financial System", "file": "No_images_dataBCOMBM/Indian Financial Systmem -Calicult University.pdf.json"},
                    {"title": "Investment Analysis", "file": "No_images_dataBCOMBM/Investment Analysis and Portfolio Management_TYBMS V 2016-17.pdf.json"}
                ],
                "Computerized Accounting": [
                    {"title": "Tally ERP 9", "file": "No_images_dataBCOMBM/Tally ERP 9 At A Glance (Tally) (Z-Library).pdf.json"},
                    {"title": "Mastering Tally Prime", "file": "No_images_dataBCOMBM/Mastering Tally PRIME Training, Certification  Job (ASOK K. NADHANI) (Z-Library).pdf.json"},
                    {"title": "Tally ERP 9 + GST", "file": "No_images_dataBCOMBM/Tally ERP 9 + GST Implementation Voucher Entries, Inventory Management, Order Processing, Taxation, and GST Accounting (Akshay Rajgaria) (Z-Library).pdf.json"}
                ]
            },
            "Semester 6": {
                "Principles and Practices of Costing": [
                    {"title": "Cost Accounting (Jawahar Lal)", "file": "No_images_dataBCOMBM/Cost accounting (Jawahar Lal Seema Srivastava) (Z-Library).pdf.json"},
                    {"title": "Financial Cost Accounting", "file": "No_images_dataBCOMBM/Textbook of Financial Cost and Management Accounting (Periasami P.) (Z-Library).pdf.json"}
                ],
                "Taxation - II": [
                    {"title": "Direct Taxation", "file": "No_images_dataBCOMBM/Direct Taxation.pdf.json"}
                ],
                "E - Banking and Cyber Laws": [
                    {"title": "E Banking", "file": "No_images_dataBCOMBM/E Banking.pdf.json"},
                    {"title": "E Banking", "file": "No_images_dataBCOMBM/E Banking _ ILIDE.INFO Platform PDF Viewer.pdf.json"},
                    {"title": "Cyber Laws", "file": "No_images_dataBCOMBM/cyber-laws-chapter-in-legal-aspects-book.pdf.json"}
                ],
                "Treasury Management": [
                    {"title": "Treasury Management", "file": "No_images_dataBCOMBM/Treasury Management Theory and Practice-TB.pdf.json"},
                    {"title": "Financial Treasury Management", "file": "No_images_dataBCOMBM/FTFM_Final.pdf.json"}
                ],
                "Investment Management": [
                    {"title": "Investment Management (Avadhani)", "file": "No_images_dataBCOMBM/Investment Management (V.A. Avadhani) (Z-Library).pdf.json"},
                    {"title": "Investment Management (Hiriyappa)", "file": "No_images_dataBCOMBM/Investment Management Securities and Portfolio Management (Dr. B. Hiriyappa) (Z-Library).pdf.json"}
                ],
                "Finanacial Management": [
                    {"title": "Financial Accounting-BMS", "file": "No_images_dataBCOMBM/Financial Accounting - BMS.pdf.json"},
                    {"title": "Financial Accounting ICAI", "file": "No_images_dataBCOMBM/Financial Accounting ICAI.pdf.json"},
                    {"title": "Financial Accounting", "file": "No_images_dataBCOMBM/Financial Accounting.pdf.json"},
                    {"title": "Financial Management (Ashish Kumar Sana)", "file": "No_images_dataBCOMBM/Financial Management (Ashish Kumar Sana) (Z-Library).pdf.json"},
                    {"title": "Financial Management (Abhishek Sharma)", "file": "No_images_dataBCOMBM/Financial Management (Abhishek Sharma) (Z-Library).pdf.json"},
                    {"title": "Financial Management (C. Paramasivan, T. Subramanian)", "file": "No_images_dataBCOMBM/Financial Management (C. Paramasivan, T. Subramanian) (Z-Library).pdf.json"},
                    {"title": "Fundamentals of Financial Management (Vyuptakesh Sharan)", "file": "No_images_dataBCOMBM/Fundamentals of Financial Management (Vyuptakesh Sharan) (Z-Library).pdf.json"},
                ],
            }
        }
    },
    "Bachelor of Commerce (CS)": {
        "1st Year": {
            "Semester 1": {
                "ADVANCED ACCOUNTANCY I & II": [
                    {"title": "Financial Accounting 1", "file": "No_images_dataBCOMCS/financial accounting 1.pdf.json"},
                    {"title": "Financial Accounting 2", "file": "No_images_dataBCOMCS/financial accounting 2.pdf.json"},
                    {"title": "Financial Accounting 3", "file": "No_images_dataBCOMCS/financial accounting 3.pdf.json"},
                    {"title": "Advanced Accountancy - I", "file": "No_images_dataBCOMCS/Advanced Accountancy - I.pdf.json"}
                ],
                "Business Regulatory Framework": [
                    {"title": "Business Regulatory Framework 1", "file": "No_images_dataBCOMCS/Business Regulatory Framework 1.pdf.json"},
                    {"title": "Business Regulatory FrameWork 2", "file": "No_images_dataBCOMCS/Business Regulatory FrameWork 2.pdf.json"},
                    {"title": "Business Regulatory FrameWork 3", "file": "No_images_dataBCOMCS/Business Regulatory FrameWork 3.pdf.json"},
                    {"title": "Indian Contract Act - Bailment and Pledge", "file": "No_images_dataBCOMCS/Indian Contract Act - Bailment and Pledge.pdf.json"},
                    {"title": "Indian Contract Act - Breach of Contract", "file": "No_images_dataBCOMCS/Indian Contract Act - Breach of Contract - CA Material.pdf.json"},
                    {"title": "Indian Contract Act - CA Foundation", "file": "No_images_dataBCOMCS/Indian Contract Act - CA Foundation material.pdf.json"},
                    {"title": "Indian Contract Act - Consideration", "file": "No_images_dataBCOMCS/Indian Contract Act - Chapter - Consideration - CA Material.pdf.json"},
                    {"title": "Indian Contract Act - Contingent and Quasi Contract", "file": "No_images_dataBCOMCS/Indian Contract Act - Contingent and Quasi Contract - CA Material.pdf.json"},
                    {"title": "Indian Contract Act - Essential Elements", "file": "No_images_dataBCOMCS/Indian Contract Act - Essential Elements of Contract - CA Material.pdf.json"},
                    {"title": "Indian Contract Act - Indemnity and Guarantee", "file": "No_images_dataBCOMCS/Indian Contract Act - Indemnity and Guarantee.pdf.json"},
                    {"title": "Indian Contract Act - Performance of Contract", "file": "No_images_dataBCOMCS/Indian Contract Act - Performance of Contract - CA Material.pdf.json"},
                    {"title": "Elements of Mercantile Law - Book 1", "file": "No_images_dataBCOMCS/Elements of Mercantile Law - Book 1 of 2.pdf.json"}
                ],
            },
            "Semester 2": {
                "Economic & Commercial Laws": [
                    {"title": "Economic Business and Commercial Laws", "file": "No_images_dataBCOMCS/Economic Business and Commercial Laws (3).pdf.json"},
                    {"title": "Elements of Mercantile Law - Book 2", "file": "No_images_dataBCOMCS/Elements of Mercantile Law - Book 2 of 2.pdf.json"},
                    {"title": "E-BOOK IPR", "file": "No_images_dataBCOMCS/E-BOOK IPR (1).pdf.json"}
                ],
                "ADVANCED ACCOUNTANCY I & II": [
                    {"title": "Financial Accounting 1", "file": "No_images_dataBCOMCS/financial accounting 1.pdf.json"},
                    {"title": "Financial Accounting 2", "file": "No_images_dataBCOMCS/financial accounting 2.pdf.json"},
                    {"title": "Financial Accounting 3", "file": "No_images_dataBCOMCS/financial accounting 3.pdf.json"},
                    {"title": "Advanced Accountancy - I", "file": "No_images_dataBCOMCS/Advanced Accountancy - I.pdf.json"}
                ],
            }
        },
        "2nd Year": {
            "Semester 3": {
                "ACCOUNTING FOR COMPANIES I & II": [
                    {"title": "Corporate Accounting 1", "file": "No_images_dataBCOMCS/Corporate Accounting 1.pdf.json"},
                    {"title": "Corporate Accounting 2", "file": "No_images_dataBCOMCS/Corporate Accounting 2.pdf.json"},
                    {"title": "Corporate Accounting 3", "file": "No_images_dataBCOMCS/Corporate Accounting 3.pdf.json"},
                    {"title": "Corporate Accounting 1 of 2", "file": "No_images_dataBCOMCS/Corporate Accounting 1 of 2 (1000 Pages).pdf.json"},
                    {"title": "Corporate Accounting 2 of 2", "file": "No_images_dataBCOMCS/Corporate Accounting 2 of 2.pdf.json"},
                ],
                "COMPANY LAW AND SECRETARIAL PRACTICE I & II": [
                    {"title": "Company Law 1", "file": "No_images_dataBCOMCS/Company Law 1.pdf.json"},
                    {"title": "Company Law 2", "file": "No_images_dataBCOMCS/Company Law 2.pdf.json"},
                    {"title": "Company Law 3", "file": "No_images_dataBCOMCS/Company Law 3.pdf.json"}
                ],
                "ETHICAL MANAGEMENT THEORY": [ 
                    {"title": "Ethical Management Theory 1", "file": "No_images_dataBCOMCS/Ethical management theory 1.pdf.json"},
                    {"title": "Ethical Management Theory 2", "file": "No_images_dataBCOMCS/Ethical management theory 2.pdf.json"},
                    {"title": "Ethical Management Theory", "file": "No_images_dataBCOMCS/Ethical Management Theory.pdf.json"}
                ],
                "DIGITAL DATA PROTECTION":[
                    {"title": "Digital Data Protection 1", "file": "No_images_dataBCOMCS/Digital Data Protection 1.pdf.json"},
                    {"title": "Digital Data Protection 2", "file": "No_images_dataBCOMCS/Digital Data Protection 2.pdf.json"},
                ]
            },
            "Semester 4": {
                "AUDITING AND ASSURANCE": [
                    {"title": "Auditing 1", "file": "No_images_dataBCOMCS/Auditing 1.pdf.json"},
                    {"title": "Auditing 2", "file": "No_images_dataBCOMCS/Auditing 2.pdf.json"}
                ],
                "SECURITIES LAWS AND FINANCIAL MARKETS": [
                    {"title": "Securities Law 1", "file": "No_images_dataBCOMCS/Securities Law 1.pdf.json"},
                    {"title": "Securities Law 2", "file": "No_images_dataBCOMCS/Securities Law 2.pdf.json"},
                    {"title": "Securities Law 3", "file": "No_images_dataBCOMCS/Securities Law 3.pdf.json"}
                ],
                "DRAFTING AND PLEADING ETQUETTE":[
                      {"title": "Drafting 1", "file": "No_images_dataBCOMCS/Drafting 1.pdf.json"},
                ]
            }
        },
        "3rd Year": {
            "Semester 5": {
                "ELEMENTS OF BUSINESS TAXATION": [
                    {"title": "Business Taxation 1", "file": "No_images_dataBCOMCS/Business Taxation 1.pdf.json"},
                    {"title": "Business Taxation 2", "file": "No_images_dataBCOMCS/Business Taxation 2.pdf.json"},
                    {"title": "Business Taxation 3", "file": "No_images_dataBCOMCS/Business Taxation 3.pdf.json"},
                    {"title": "Business Taxation 4", "file": "No_images_dataBCOMCS/Business Taxation 4.pdf.json"},
                    {"title": "Income Tax 1", "file": "No_images_dataBCOMCS/Income Tax 1.pdf.json"},
                    {"title": "Income Tax 2", "file": "No_images_dataBCOMCS/Income Tax 2.pdf.json"},
                    {"title": "Income Tax 3", "file": "No_images_dataBCOMCS/Income Tax 3.pdf.json"}
                ],
                "ENTREPRENEURSHIP & SMALL BUSINESS MANAGEMENT": [
                    {"title": "Entrepreneurship 1", "file": "No_images_dataBCOMCS/Entrepreneurship 1.pdf.json"},
                    {"title": "Entrepreneurship 2", "file": "No_images_dataBCOMCS/Entrepreneurship 2.pdf.json"},
                    {"title": "Entrepreneurship 3", "file": "No_images_dataBCOMCS/Entrepreneurship 3.pdf.json"},
                    {"title": "Entrepreneurship & Small Business", "file": "No_images_dataBCOMCS/Entrepreneurship and Small Business Management.pdf.json"}
                ],
                "INDUSTRIAL & LABOUR LAWS": [
                    {"title": "Industrial and Labour laws 1", "file": "No_images_dataBCOMCS/Industrial and Labour laws 1.pdf.json"},
                    {"title": "Industrial and Labour laws 2", "file": "No_images_dataBCOMCS/Industrial and Labour laws 2.pdf.json"},
                    {"title": "Industrial and Labour laws 3", "file": "No_images_dataBCOMCS/Industrial and Labour laws 3.pdf.json"},
                ],
                "PRINCIPLES OF COSTING":[
                      {"title": "Costing 1", "file": "No_images_dataBCOMCS/costing 1.pdf.json"},
                    {"title": "Costing 2", "file": "No_images_dataBCOMCS/costing 2.pdf.json"},
                    {"title": "Costing 3", "file": "No_images_dataBCOMCS/costing 3.pdf.json"}
                ]
            },
            "Semester 6": {
                "PRINCIPLES OF MANAGEMENT ACCOUNTING": [
                   
                    {"title": "Management Accounting 1", "file": "No_images_dataBCOMCS/Management Accounting 1.pdf.json"},
                    {"title": "Management Accounting 2", "file": "No_images_dataBCOMCS/Management Accounting 2.pdf.json"},
                    {"title": "Management Accounting 3", "file": "No_images_dataBCOMCS/Management Accounting 3.pdf.json"},
                    {"title": "MA Part 1", "file": "No_images_dataBCOMCS/MA Part 1.pdf.json"},
                    {"title": "MA Part 2", "file": "No_images_dataBCOMCS/MA Part 2.pdf.json"},
                    {"title": "MA Part 3", "file": "No_images_dataBCOMCS/MA Part 3.pdf.json"},
                    {"title": "MA Part 4", "file": "No_images_dataBCOMCS/MA Part 4.pdf.json"}
                ],
                "CORPORATE FINANCE":[
                      {"title": "Financial Management 1", "file": "No_images_dataBCOMCS/FinancialManagement 1.pdf.json"},
                    {"title": "Financial Management 2", "file": "No_images_dataBCOMCS/FinancialManagement 2.pdf.json"},
                    {"title": "Financial Management 3", "file": "No_images_dataBCOMCS/FinancialManagement 3.pdf.json"},
                ],
                "CORPORATE HRM": [
                    {"title": "HRM 1", "file": "No_images_dataBCOMCS/HRM 1.pdf.json"},
                    {"title": "HRM 2", "file": "No_images_dataBCOMCS/HRM 2.pdf.json"},
                    {"title": "HRM 3", "file": "No_images_dataBCOMCS/HRM 3.pdf.json"},
                    {"title": "Human Resource Management - C B Gupta", "file": "No_images_dataBCOMCS/Human Resource Management - C B Gupta.pdf.json"}
                ],
                "PRINCIPLES OF INCOME TAX I & II":[
                     {"title": "Income Tax 1", "file": "No_images_dataBCOMCS/Income Tax 1.pdf.json"},
                    {"title": "Income Tax 2", "file": "No_images_dataBCOMCS/Income Tax 2.pdf.json"},
                    {"title": "Income Tax 3", "file": "No_images_dataBCOMCS/Income Tax 3.pdf.json"}
                ]
            }
        }
    },
    "Bachelor of Commerce (ISM)":{
        "1st Year":{
            "Semester 1":{
                "Financial Accounting and IFRS":[
                     {"title": "Auditing & Assurance", "file": "No_images_dataBCOMISM/Auditing & Assurance.pdf.json"},
                     {"title": "Cost and Management Accounting(First 1000 pages)", "file": "No_images_dataBCOMISM/Cost and Management Accounting (First 1000 Pages).pdf.json"},
                     {"title": "Cost and Management Accounting(Second 768 pages)", "file": "No_images_dataBCOMISM/Cost and Management Accounting (Second 748 Pages).pdf.json"},
                     {"title": "Accounting Standards ", "file": "No_images_dataBCOMISM/Accounting Standards.pdf.json"},
                     {"title": "FA Unit 1A ", "file": "No_images_dataBCOMISM/FA Unit 1A.pdf.json"},
                     {"title": "FA Unit 1B ", "file": "No_images_dataBCOMISM/FA Unit 1B.pdf.json"},
                     {"title": "FA Unit 2 ", "file": "No_images_dataBCOMISM/FA Unit 2.pdf.json"},
                     {"title": "FA Unit 3 ", "file": "No_images_dataBCOMISM/FA Unit 3.pdf.json"},
                     {"title": "FA Unit 4 ", "file": "No_images_dataBCOMISM/FA Unit 4.pdf.json"},
                     {"title": "FA Unit 5 ", "file": "No_images_dataBCOMISM/FA Unit 5.pdf.json"},
                ],

            },
            "Semester 2":{
                "Corporate Accounting":[
                     {"title": "Unit 1 ", "file": "No_images_dataBCOMISM/Unit 1.pdf.json"},
                     {"title": "Unit 2 ", "file": "No_images_dataBCOMISM/Unit 2.pdf.json"},
                     {"title": "Unit 3 ", "file": "No_images_dataBCOMISM/Unit 3.pdf.json"},
                     {"title": "Unit 4 ", "file": "No_images_dataBCOMISM/Unit 4.pdf.json"},
                     {"title": "Unit 5 ", "file": "No_images_dataBCOMISM/Unit 5.pdf.json"},
                ]
            }
        },
        "3rd Year":{
            "Semester 5":{
                "Direct Taxation":[
                     {"title": "Part 1 ", "file": "No_images_dataBCOMISM/Part 1.pdf.json"},
                     {"title": "Part 2A ", "file": "No_images_dataBCOMISM/Part 2A.pdf.json"},
                     {"title": "Part 2B ", "file": "No_images_dataBCOMISM/Part 2B.pdf.json"},
                     {"title": "Part 2C ", "file": "No_images_dataBCOMISM/Part 2C.pdf.json"},
                     {"title": "Part 2D ", "file": "No_images_dataBCOMISM/Part 2D.pdf.json"},
                     {"title": "Part 3 ", "file": "No_images_dataBCOMISM/Part 3.pdf.json"},
                     {"title": "Part 4A ", "file": "No_images_dataBCOMISM/Part 4A.pdf.json"},
                     {"title": "Part 4B ", "file": "No_images_dataBCOMISM/Part 4B.pdf.json"},
                     {"title": "Part 5 ", "file": "No_images_dataBCOMISM/Part 5.pdf.json"},
                     {"title": "Part 6 ", "file": "No_images_dataBCOMISM/Part 6.pdf.json"},
                ]
            }
        }
    }
}


def resolve_files(year, branch, semester, subject, base_directory="."):
    """
    Determines the list of filenames to search in ChromaDB based on subject selection.
    
    Args:
        year (str): Academic year (e.g., "1st Year", "2nd Year")
        branch (str): Course branch (e.g., "Bachelor of Business Administration")
        semester (str): Semester (e.g., "Semester 1", "Semester 2")
        subject (str): Subject name (e.g., "Marketing Management")
        base_directory (str): Base directory where files are located
        
    Returns:
        list: List of file paths that exist for this subject
    """
    # Ensure inputs are strings
    year = str(year) if year else ""
    branch = str(branch) if branch else ""
    semester = str(semester) if semester else ""
    subject = str(subject) if subject else ""

    # Try to find exact match in ACADEMIC_CONFIG
    try:
        book_list = ACADEMIC_CONFIG[branch][year][semester][subject]
        
        # Filter to only existing files
        existing_files = []
        for book in book_list:
            file_path = os.path.join(base_directory, book['file'])
            if os.path.exists(file_path):
                existing_files.append(book['file'])
        
        if existing_files:
            print(f"[Config] Found {len(existing_files)} files for {subject}")
            return existing_files
    except KeyError:
        print(f"[Config] No mapping found for {branch} -> {year} -> {semester} -> {subject}")
    
    # Fallback: return empty list (no files found)
    print(f"[Config] No files available for this subject")
    return []


def get_source_filters(year, branch, semester, subject, base_directory="."):
    """
    Gets the list of 'source' metadata values from the JSON files.
    This is used to filter ChromaDB queries to only search within relevant documents.
    
    Args:
        year (str): Academic year
        branch (str): Course branch
        semester (str): Semester
        subject (str): Subject name
        base_directory (str): Base directory where files are located
        
    Returns:
        list: List of source filenames to use in ChromaDB where filter
    """
    import json
    
    files = resolve_files(year, branch, semester, subject, base_directory)
    sources = []
    
    for file_path in files:
        full_path = os.path.join(base_directory, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    if 'metadata' in data[0] and 'source' in data[0]['metadata']:
                        src = data[0]['metadata']['source']
                        if src not in sources:
                            sources.append(src)
        except Exception as e:
            print(f"[Config] Error reading source from {file_path}: {e}")
    
    return sources


def get_subject_files(year, branch, semester, subject, base_directory="."):
    """
    Returns the list of book dictionaries (title, file) for a given subject.
    """
    # Ensure inputs are strings
    year = str(year) if year else ""
    branch = str(branch) if branch else ""
    semester = str(semester) if semester else ""
    subject = str(subject) if subject else ""

    try:
        book_list = ACADEMIC_CONFIG[branch][year][semester][subject]
        return book_list
    except KeyError:
        return []
