# 🕵️‍♂️ SEO Audit Tool – Local SEO & Performance Analyzer

**SEO Audit Tool** is a complete command-line tool for auditing websites' on-page SEO performance and generating a comprehensive PDF report. Built with ❤️ by [Abin Vinod](https://github.com/abinvinod) under the banner of **Sysdevcode**.

---

## 🚀 Features

- ✅ Title & Meta Description Analysis  
- ✅ Keyword Frequency (Title, Headings, Body)  
- ✅ H1 Tags Count & Status  
- ✅ Image ALT Tag Audit  
- ✅ Schema Markup Detection (JSON-LD, Microdata, RDFa)  
- ✅ PageSpeed Insights Integration  
- ✅ Professional PDF Report Generation  
- ✅ Branding support (your logo in PDF)

---

## 📂 Project Structure

```

seo-audit-tool/
│
├── seo.py                  # Main Python script
├── requirements.txt        # Required dependencies
├── assets/
│   └── lo.png              # Logo (included in PDF)
└── README.md               # Project description

````

---

## 🛠️ Installation

1. **Clone the repo:**
```bash
git clone https://github.com/YOUR_USERNAME/seo-audit-tool.git
cd seo-audit-tool
````

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Add your logo:**
   Place your logo as `lo.png` inside the `assets/` folder. This will be added to the bottom of the PDF.

---

## 🔑 PageSpeed API Setup (Optional)

For performance scoring:

1. Visit: [Google PageSpeed API Docs](https://developers.google.com/speed/docs/insights/v5/get-started)
2. Enable the API and copy your key
3. Paste it when the program prompts you

---

## ▶️ How to Use

```bash
python seo.py
```

Then:

* Enter your API key (optional)
* Provide the website URL and target keyword
* Wait for analysis
* A PDF report will be saved in your folder

---

## 📊 Report Includes

* Title and meta description length & content
* Keyword density stats
* H1 tag content and structure
* ALT tag presence on images
* Schema markup types
* Google PageSpeed performance score
* Logo branding at the bottom

---

## 👨‍💻 Built With

* Python 3.x
* requests
* beautifulsoup4
* fpdf2

---

## 🔖 License

This project is licensed under the MIT License.

---

## ✨ Credits

**Author**: [Abin Vinod](https://github.com/abinvinod)
**Organization**: [Sysdevcode](https://sysdevcode.com)
**Motto**: *Code to Create. Dream to Build.*
