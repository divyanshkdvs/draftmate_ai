"""
Legal Authority and Citation Database for DraftMate AI
Contains indexed landmark judicial precedents, statutory codes, and institutional source links.
"""

from typing import Dict, Any, Optional

# Verified Legal Precedents Index
VERIFIED_PRECEDENTS = {
    "puttaswamy": {
        "title": "Justice K.S. Puttaswamy (Retd.) and Anr. v. Union of India and Ors.",
        "citation": "(2017) 10 SCC 1",
        "alternate_citations": ["AIR 2017 SC 4161", "2017 10 SCC 1"],
        "court": "Supreme Court of India (9-Judge Constitution Bench)",
        "year": 2017,
        "status": "Verified - Binding Law",
        "subject": "Fundamental Right to Privacy under Article 21; Proportionality Standard",
        "source_url": "https://main.sci.gov.in/supremecourt/2012/35071/35071_2012_Judgement_24-Aug-2017.pdf"
    },
    "kesavananda": {
        "title": "Kesavananda Bharati Sripadagalvaru v. State of Kerala",
        "citation": "(1973) 4 SCC 225",
        "alternate_citations": ["AIR 1973 SC 1461"],
        "court": "Supreme Court of India (13-Judge Constitution Bench)",
        "year": 1973,
        "status": "Verified - Landmark Precedent",
        "subject": "Basic Structure Doctrine; Parliamentary amending power under Article 368",
        "source_url": "https://indiankanoon.org/doc/257876/"
    },
    "maneka gandhi": {
        "title": "Maneka Gandhi v. Union of India",
        "citation": "(1978) 1 SCC 248",
        "alternate_citations": ["AIR 1978 SC 597"],
        "court": "Supreme Court of India (7-Judge Bench)",
        "year": 1978,
        "status": "Verified - Binding Law",
        "subject": "Procedure Established by Law must be Just, Fair, and Reasonable under Article 21",
        "source_url": "https://indiankanoon.org/doc/1766147/"
    },
    "saw pipes": {
        "title": "Oil & Natural Gas Corporation Ltd. v. Saw Pipes Ltd.",
        "citation": "(2003) 5 SCC 705",
        "alternate_citations": ["AIR 2003 SC 2629"],
        "court": "Supreme Court of India",
        "year": 2003,
        "status": "Verified - Commercial Law Precedent",
        "subject": "Arbitration awards; Liquidated damages under Section 73 & 74 Indian Contract Act",
        "source_url": "https://indiankanoon.org/doc/157297/"
    },
    "zaheer khan": {
        "title": "Percept D'Mark (India) (P) Ltd. v. Zaheer Khan and Anr.",
        "citation": "(2006) 4 SCC 227",
        "alternate_citations": ["AIR 2006 SC 3426"],
        "court": "Supreme Court of India",
        "year": 2006,
        "status": "Verified - Binding Law",
        "subject": "Section 27 Indian Contract Act; Restraint of trade post-contractual termination is void",
        "source_url": "https://indiankanoon.org/doc/987114/"
    },
    "carbolic": {
        "title": "Carlill v. Carbolic Smoke Ball Co",
        "citation": "[1893] 1 QB 256",
        "alternate_citations": ["1893 1 QB 256"],
        "court": "Court of Appeal of England and Wales",
        "year": 1893,
        "status": "Verified - Common Law Foundation",
        "subject": "Unilateral contracts; Offer to the world at large; Consideration through performance",
        "source_url": "https://www.bailii.org/ew/cases/EWCA/Civ/1892/1.html"
    },
    "hadley": {
        "title": "Hadley v. Baxendale",
        "citation": "(1854) 9 Exch 341",
        "alternate_citations": ["156 ER 145"],
        "court": "Court of Exchequer (Common Law)",
        "year": 1854,
        "status": "Verified - Foundation Rule",
        "subject": "Foreseeability and Remoteness of Contractual Damages (Direct vs Consequential)",
        "source_url": "http://www.bailii.org/ew/cases/EWHC/Exch/1854/J70.html"
    },
    "salomon": {
        "title": "Salomon v. Salomon & Co Ltd",
        "citation": "[1897] AC 22",
        "alternate_citations": ["1897 AC 22"],
        "court": "House of Lords",
        "year": 1897,
        "status": "Verified - Company Law Foundation",
        "subject": "Separate Legal Personality and Corporate Veil doctrine",
        "source_url": "https://www.bailii.org/uk/cases/UKHL/1896/1.html"
    },
    "miranda": {
        "title": "Miranda v. Arizona",
        "citation": "384 U.S. 436",
        "alternate_citations": ["384 US 436", "86 S. Ct. 1602"],
        "court": "Supreme Court of the United States",
        "year": 1966,
        "status": "Verified - Constitutional Law",
        "subject": "Fifth Amendment privilege against self-incrimination; Procedural Miranda Warnings",
        "source_url": "https://supreme.justia.com/cases/federal/us/384/436/"
    }
}

# Verified Statutory Acts and Key Provisions
VERIFIED_STATUTES = {
    "indian contract act": {
        "short_name": "Indian Contract Act, 1872",
        "year": 1872,
        "jurisdiction": "India",
        "verified_sections": {
            "10": "What agreements are contracts - Free consent, competent parties, lawful consideration and object",
            "27": "Agreement in restraint of trade, void - Any agreement restraining exercising lawful profession is void",
            "28": "Agreements in restraint of legal proceedings, void",
            "73": "Compensation for loss or damage caused by breach of contract - Hadley v Baxendale rule",
            "74": "Compensation for breach of contract where penalty stipulated for - Liquidated damages"
        },
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2187"
    },
    "negotiable instruments act": {
        "short_name": "Negotiable Instruments Act, 1881",
        "year": 1881,
        "jurisdiction": "India",
        "verified_sections": {
            "138": "Dishonour of cheque for insufficiency of funds in the accounts - Criminal penalty and procedure",
            "139": "Presumption in favour of holder - Burden on drawer to rebut consideration",
            "141": "Offences by companies - Vicarious liability of directors in charge"
        },
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1895"
    },
    "companies act": {
        "short_name": "Companies Act, 2013",
        "year": 2013,
        "jurisdiction": "India",
        "verified_sections": {
            "135": "Corporate Social Responsibility (CSR) committee and mandatory spend obligations",
            "149": "Company to have Board of Directors - Independent directors and women director mandates",
            "166": "Duties of directors - Fiduciary obligation to act in good faith",
            "177": "Audit Committee composition and vigil mechanism",
            "188": "Related party transactions - Board and shareholder approval requirements",
            "403": "Fee for filing of documents and delayed filings"
        },
        "official_source": "https://www.mca.gov.in/Ministry/pdf/CompaniesAct2013.pdf"
    },
    "arbitration and conciliation act": {
        "short_name": "Arbitration and Conciliation Act, 1996",
        "year": 1996,
        "jurisdiction": "India",
        "verified_sections": {
            "7": "Arbitration agreement - Form, writing requirement, reference clauses",
            "8": "Power to refer parties to arbitration where there is an arbitration agreement",
            "9": "Interim measures by Court prior to or during arbitral proceedings",
            "11": "Appointment of arbitrators by High Court / Supreme Court",
            "34": "Application for setting aside arbitral award - Public policy grounds"
        },
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1978"
    },
    "digital personal data protection act": {
        "short_name": "Digital Personal Data Protection Act, 2023 (DPDP)",
        "year": 2023,
        "jurisdiction": "India",
        "verified_sections": {
            "4": "Grounds for processing digital personal data - Consent and legitimate uses",
            "6": "Notice and request for consent - Itemized and accessible form",
            "8": "General obligations of Data Fiduciary - Security safeguards and breach reporting",
            "9": "Processing of personal data of children - Verifiable parental consent",
            "11": "Rights of Data Principal - Right to access, correction, erasure and grievance redressal"
        },
        "official_source": "https://www.meity.gov.in/writereaddata/files/Digital%20Personal%20Data%20Protection%20Act%202023.pdf"
    },
    "bharatiya nyaya sanhita": {
        "short_name": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
        "year": 2023,
        "jurisdiction": "India",
        "verified_sections": {
            "316": "Criminal breach of trust (corresponding to legacy Sec 405 IPC)",
            "318": "Cheating and dishonestly inducing delivery of property (corresponding to legacy Sec 420 IPC)",
            "356": "Defamation and punishment for defamatory imputations"
        },
        "official_source": "https://www.mha.gov.in/sites/default/files/250883_english_01042024.pdf"
    },
    "constitution of india": {
        "short_name": "Constitution of India",
        "year": 1950,
        "jurisdiction": "India",
        "verified_sections": {
            "14": "Equality before the law and equal protection of the laws",
            "19": "Protection of certain rights regarding freedom of speech, assembly, association",
            "21": "Protection of life and personal liberty - Substantive due process & privacy",
            "32": "Remedies for enforcement of fundamental rights - Writ jurisdiction of Supreme Court",
            "226": "Power of High Courts to issue certain writs"
        },
        "official_source": "https://legislative.gov.in/constitution-of-india"
    },
    "defend trade secrets act": {
        "short_name": "Defend Trade Secrets Act (18 U.S.C. § 1836)",
        "year": 2016,
        "jurisdiction": "United States",
        "verified_sections": {
            "1836": "Civil proceedings for misappropriation of trade secrets in interstate commerce",
            "1833": "Immunity for confidential disclosure to government or in court filing"
        },
        "official_source": "https://www.govinfo.gov/app/details/USCODE-2016-title18-partI-chap90-sec1836"
    }
}
