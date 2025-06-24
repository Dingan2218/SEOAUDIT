#!/usr/bin/env python3
"""
SEO Audit Tool - Complete Local SEO Analysis Tool
Author: Assistant
Version: 1.0
"""

import requests
import re
import json
import os
import sys
from urllib.parse import urlparse, urljoin
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    from bs4 import BeautifulSoup
    from fpdf import FPDF
except ImportError:
    print("Missing required packages. Please install them using:")
    print("pip install requests beautifulsoup4 fpdf2")
    sys.exit(1)


class SEOAuditTool:
    def __init__(self):
        self.api_key = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def display_welcome(self):
        """Display welcome message and tool information"""
        print("\n" + "="*80)
        print("""
 ██████ ███████  ██████      █████  ██    ██ ██████  ██ ████████ 
██      ██      ██    ██    ██   ██ ██    ██ ██   ██ ██    ██    
██████  █████   ██    ██    ███████ ██    ██ ██   ██ ██    ██    
     ██ ██      ██    ██    ██   ██ ██    ██ ██   ██ ██    ██    
██████  ███████  ██████     ██   ██  ██████  ██████  ██    ██    

██   ██ ███████ ██    ██ ██     ██  ██████  ██████  ██████  
██  ██  ██       ██  ██  ██     ██ ██    ██ ██   ██ ██   ██ 
█████   █████     ████   ██  █  ██ ██    ██ ██████  ██   ██ 
██  ██  ██         ██    ██ ███ ██ ██    ██ ██   ██ ██   ██ 
██   ██ ███████    ██     ███ ███   ██████  ██   ██ ██████  

██████   █████  ███    ██ ██   ██ ██ ███    ██  ██████  
██   ██ ██   ██ ████   ██ ██  ██  ██ ████   ██ ██       
██████  ███████ ██ ██  ██ █████   ██ ██ ██  ██ ██   ███ 
██   ██ ██   ██ ██  ██ ██ ██  ██  ██ ██  ██ ██ ██    ██ 
██   ██ ██   ██ ██   ████ ██   ██ ██ ██   ████  ██████  
        """)
        print("="*80)
        print("           SEO AUDIT AND KEYWORD RANKING v1.0")
        print("="*80)
        print()
        print("           by sysdevcode | created by Abinvinod")
        print()
        print("="*80)
        print("📊 Features:")
        print("   ✓ Title & Meta Description Analysis")
        print("   ✓ Keyword Frequency Check")
        print("   ✓ H1 Tags Analysis")
        print("   ✓ Image & ALT Tags Audit")
        print("   ✓ Schema Markup Detection")
        print("   ✓ PageSpeed Insights Integration")
        print("   ✓ Professional PDF Reports")
        print("="*80)

    def display_menu(self):
        """Display main menu options"""
        print("\n📋 MAIN MENU:")
        print("1. Enter Google PageSpeed API Key")
        print("2. Run SEO Audit")
        print("3. Exit")
        print("-" * 30)

    def get_api_key(self):
        """Get and store Google PageSpeed API key"""
        print("\n🔑 Google PageSpeed Insights API Key Setup")
        print("-" * 45)
        print("To get your API key:")
        print("1. Visit: https://developers.google.com/speed/docs/insights/v5/get-started")
        print("2. Create a project and enable PageSpeed Insights API")
        print("3. Generate an API key")
        print()
        
        api_key = input("Enter your Google PageSpeed API Key (or press Enter to skip): ").strip()
        
        if api_key:
            self.api_key = api_key
            print("✅ API Key saved successfully!")
        else:
            print("⚠️  No API Key provided. PageSpeed analysis will be skipped.")

    def get_page_content(self, url: str) -> Tuple[Optional[BeautifulSoup], Optional[str]]:
        """Fetch and parse webpage content"""
        try:
            print(f"🌐 Fetching content from: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup, response.text
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching URL: {str(e)}")
            return None, None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None, None

    def extract_title_tag(self, soup: BeautifulSoup) -> str:
        """Extract title tag from webpage"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else "No title tag found"

    def extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description from webpage"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc.get('content').strip()
        return "No meta description found"

    def calculate_keyword_frequency(self, html_content: str, keyword: str) -> Dict[str, int]:
        """Calculate keyword frequency in different parts of the page"""
        if not html_content or not keyword:
            return {'total': 0, 'title': 0, 'headings': 0, 'body': 0}

        soup = BeautifulSoup(html_content, 'html.parser')
        keyword_lower = keyword.lower()
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get all text content
        all_text = soup.get_text().lower()
        total_count = all_text.count(keyword_lower)
        
        # Title count
        title_text = soup.find('title')
        title_count = title_text.get_text().lower().count(keyword_lower) if title_text else 0
        
        # Headings count (h1-h6)
        headings_text = ' '.join([h.get_text().lower() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        headings_count = headings_text.count(keyword_lower)
        
        # Body count (excluding title and headings)
        body_count = max(0, total_count - title_count - headings_count)
        
        return {
            'total': total_count,
            'title': title_count,
            'headings': headings_count,
            'body': body_count
        }

    def analyze_h1_tags(self, soup: BeautifulSoup) -> Dict[str, any]:
        """Analyze H1 tags on the page"""
        h1_tags = soup.find_all('h1')
        h1_texts = [h1.get_text().strip() for h1 in h1_tags]
        
        return {
            'count': len(h1_tags),
            'texts': h1_texts,
            'status': 'Good' if len(h1_tags) == 1 else 'Warning | It is generally recommended to only use one H1 Tag on a page.' if len(h1_tags) > 1 else 'Missing'
        }

    def analyze_images(self, soup: BeautifulSoup, base_url: str) -> Dict[str, int]:
        """Analyze images and ALT tags"""
        images = soup.find_all('img')
        total_images = len(images)
        missing_alt = 0
        
        for img in images:
            alt_text = img.get('alt', '').strip()
            if not alt_text:
                missing_alt += 1
        
        return {
            'total_images': total_images,
            'missing_alt': missing_alt,
            'with_alt': total_images - missing_alt
        }

    def check_schema_markup(self, soup: BeautifulSoup) -> Dict[str, any]:
        """Check for schema markup presence"""
        # Check for JSON-LD
        json_ld = soup.find_all('script', type='application/ld+json')
        
        # Check for microdata
        microdata = soup.find_all(attrs={'itemscope': True})
        
        # Check for RDFa
        rdfa = soup.find_all(attrs={'typeof': True})
        
        has_schema = len(json_ld) > 0 or len(microdata) > 0 or len(rdfa) > 0
        
        schema_types = []
        
        # Extract schema types from JSON-LD
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and '@type' in data:
                    schema_types.append(data['@type'])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@type' in item:
                            schema_types.append(item['@type'])
            except (json.JSONDecodeError, TypeError):
                continue
        
        return {
            'has_schema': has_schema,
            'json_ld_count': len(json_ld),
            'microdata_count': len(microdata),
            'rdfa_count': len(rdfa),
            'schema_types': list(set(schema_types))
        }

    def get_pagespeed_insights(self, url: str) -> Optional[Dict[str, any]]:
        """Get PageSpeed Insights data from Google API"""
        if not self.api_key:
            return None
        
        try:
            print("⚡ Analyzing PageSpeed Performance...")
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            params = {
                'url': url,
                'key': self.api_key,
                'category': 'performance'
            }
            
            response = requests.get(api_url, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            lighthouse_result = data.get('lighthouseResult', {})
            categories = lighthouse_result.get('categories', {})
            performance = categories.get('performance', {})
            
            audits = lighthouse_result.get('audits', {})
            fcp_audit = audits.get('first-contentful-paint', {})
            
            return {
                'performance_score': int(performance.get('score', 0) * 100) if performance.get('score') else 0,
                'fcp': fcp_audit.get('displayValue', 'N/A'),
                'fcp_numeric': fcp_audit.get('numericValue', 0)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  PageSpeed API Error: {str(e)}")
            return None
        except Exception as e:
            print(f"⚠️  PageSpeed Analysis Error: {str(e)}")
            return None

    def run_audit(self):
        """Main audit function"""
        print("\n🔍 SEO AUDIT ANALYZER")
        print("-" * 25)
        
        # Get URL
        url = input("Enter website URL (with https://): ").strip()
        if not url.startswith(('http://', 'https://')):
            print("❌ Please enter a valid URL starting with http:// or https://")
            return
        
        # Get keyword
        keyword = input("Enter keyword to analyze: ").strip()
        if not keyword:
            print("❌ Keyword cannot be empty")
            return
        
        print(f"\n🚀 Starting SEO audit for: {url}")
        print(f"🎯 Target keyword: '{keyword}'")
        print("-" * 50)
        
        # Fetch page content
        soup, html_content = self.get_page_content(url)
        if not soup:
            return
        
        # Extract domain for filename
        domain = urlparse(url).netloc.replace('www.', '')
        
        # Perform all analyses
        print("📊 Analyzing SEO elements...")
        
        results = {
            'url': url,
            'keyword': keyword,
            'domain': domain,
            'audit_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'title_tag': self.extract_title_tag(soup),
            'meta_description': self.extract_meta_description(soup),
            'keyword_frequency': self.calculate_keyword_frequency(html_content, keyword),
            'h1_analysis': self.analyze_h1_tags(soup),
            'image_analysis': self.analyze_images(soup, url),
            'schema_analysis': self.check_schema_markup(soup),
            'pagespeed_data': self.get_pagespeed_insights(url)
        }
        
        # Display results
        self.display_results(results)
        
        # Generate PDF report
        pdf_filename = f"SEO_Audit_Report_{domain}.pdf"
        if self.generate_pdf_report(results, pdf_filename):
            print(f"\n✅ Audit completed successfully!")
            print(f"📄 PDF report saved as: {pdf_filename}")
        else:
            print("\n⚠️  Audit completed but PDF generation failed.")
        
        input("\nPress Enter to return to main menu...")

    def display_results(self, results: Dict):
        """Display audit results in console"""
        print("\n" + "="*60)
        print("📋 SEO AUDIT RESULTS")
        print("="*60)
        
        print(f"🌐 URL: {results['url']}")
        print(f"🎯 Keyword: {results['keyword']}")
        print(f"📅 Date: {results['audit_date']}")
        print("-" * 60)
        
        # Title Tag
        print(f"📰 Title Tag: {results['title_tag']}")
        print(f"   Length: {len(results['title_tag'])} characters")
        
        # Meta Description
        print(f"📝 Meta Description: {results['meta_description']}")
        print(f"   Length: {len(results['meta_description'])} characters")
        
        # Keyword Frequency
        kf = results['keyword_frequency']
        print(f"🔍 Keyword Frequency:")
        print(f"   Total occurrences: {kf['total']}")
        print(f"   In title: {kf['title']}")
        print(f"   In headings: {kf['headings']}")
        print(f"   In body: {kf['body']}")
        
        # H1 Analysis
        h1 = results['h1_analysis']
        print(f"📊 H1 Tags Analysis:")
        print(f"   Count: {h1['count']} ({h1['status']})")
        if h1['texts']:
            for i, h1_text in enumerate(h1['texts'], 1):
                print(f"   H1 {i}: {h1_text[:60]}{'...' if len(h1_text) > 60 else ''}")
        
        # Images
        img = results['image_analysis']
        print(f"🖼️  Images Analysis:")
        print(f"   Total images: {img['total_images']}")
        print(f"   With ALT tags: {img['with_alt']}")
        print(f"   Missing ALT tags: {img['missing_alt']}")
        
        # Schema Markup
        schema = results['schema_analysis']
        print(f"🏗️  Schema Markup:")
        print(f"   Present: {'Yes' if schema['has_schema'] else 'No'}")
        if schema['has_schema']:
            print(f"   JSON-LD: {schema['json_ld_count']}")
            print(f"   Microdata: {schema['microdata_count']}")
            if schema['schema_types']:
                print(f"   Schema Types: {', '.join(schema['schema_types'])}")
        
        # PageSpeed
        if results['pagespeed_data']:
            ps = results['pagespeed_data']
            print(f"⚡ PageSpeed Performance:")
            print(f"   Performance Score: {ps['performance_score']}/100")
            print(f"   First Contentful Paint: {ps['fcp']}")
        else:
            print("⚡ PageSpeed Performance: Not available (API key not provided)")

    def generate_pdf_report(self, results: Dict, filename: str) -> bool:
        """Generate PDF report with vertical layout"""
        try:
            print("📄 Generating PDF report...")
            
            from fpdf import FPDF
            
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font('Helvetica', 'B', 16)
            pdf.ln(10)
            pdf.cell(0, 10, 'SEO AUDIT REPORT', 0, 1, 'C')
            pdf.ln(5)
            
            # Basic Info Section
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'WEBSITE INFORMATION', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            # Split long URLs into multiple lines
            url_parts = results['url'].replace('https://', '').replace('http://', '')
            if len(url_parts) > 50:
                pdf.cell(0, 6, 'Website:', 0, 1)
                pdf.cell(0, 6, f"  {url_parts[:50]}", 0, 1)
                if len(url_parts) > 50:
                    pdf.cell(0, 6, f"  {url_parts[50:]}", 0, 1)
            else:
                pdf.cell(0, 6, f"Website: {url_parts}", 0, 1)
            
            pdf.cell(0, 6, f"Keyword: {results['keyword']}", 0, 1)
            pdf.cell(0, 6, f"Date: {results['audit_date']}", 0, 1)
            pdf.ln(8)
            
            # Title Analysis
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'TITLE TAG ANALYSIS | Optimal length (between 50 and 60 characters).', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            # Break title into multiple lines if too long
            title = results['title_tag']
            if len(title) > 70:
                pdf.cell(0, 6, 'Title:', 0, 1)
                words = title.split()
                line = ""
                for word in words:
                    if len(line + word) < 65:
                        line += word + " "
                    else:
                        pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
                        line = word + " "
                if line.strip():
                    pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
            else:
                pdf.cell(0, 6, f"Title: {title}", 0, 1)
            
            pdf.cell(0, 6, f"Length: {len(title)} characters", 0, 1)
            pdf.ln(6)
            
            # Meta Description Analysis
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'META DESCRIPTION ANALYSIS', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            # Break description into multiple lines
            desc = results['meta_description']
            if len(desc) > 70:
                pdf.cell(0, 6, 'Description:', 0, 1)
                words = desc.split()
                line = ""
                for word in words:
                    if len(line + word) < 65:
                        line += word + " "
                    else:
                        pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
                        line = word + " "
                if line.strip():
                    pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
            else:
                pdf.cell(0, 6, f"Description: {desc}", 0, 1)
            
            pdf.cell(0, 6, f"Length: {len(desc)} characters", 0, 1)
            pdf.ln(6)
            
            # Keyword Frequency
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'KEYWORD FREQUENCY', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            kf = results['keyword_frequency']
            pdf.cell(0, 6, f"Total Occurrences: {kf['total']}", 0, 1)
            pdf.cell(0, 6, f"In Title: {kf['title']}", 0, 1)
            pdf.cell(0, 6, f"In Headings: {kf['headings']}", 0, 1)
            pdf.cell(0, 6, f"In Body Text: {kf['body']}", 0, 1)
            pdf.ln(6)
            
            # H1 Tags Analysis
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'H1 TAGS ANALYSIS', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            h1 = results['h1_analysis']
            pdf.cell(0, 6, f"H1 Count: {h1['count']}", 0, 1)
            pdf.cell(0, 6, f"Status: {h1['status']}", 0, 1)
            
            for i, h1_text in enumerate(h1['texts'], 1):
                pdf.cell(0, 6, f"H1 #{i}:", 0, 1)
                # Break H1 text into lines
                if len(h1_text) > 60:
                    words = h1_text.split()
                    line = ""
                    for word in words:
                        if len(line + word) < 55:
                            line += word + " "
                        else:
                            pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
                            line = word + " "
                    if line.strip():
                        pdf.cell(0, 6, f"  {line.strip()}", 0, 1)
                else:
                    pdf.cell(0, 6, f"  {h1_text}", 0, 1)
            pdf.ln(6)
            
            # Images Analysis
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'IMAGES ANALYSIS', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            img = results['image_analysis']
            pdf.cell(0, 6, f"Total Images: {img['total_images']}", 0, 1)
            pdf.cell(0, 6, f"With ALT Tags: {img['with_alt']}", 0, 1)
            pdf.cell(0, 6, f"Missing ALT Tags: {img['missing_alt']}", 0, 1)
            pdf.ln(6)
            
            # Schema Markup
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'SCHEMA MARKUP', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            schema = results['schema_analysis']
            pdf.cell(0, 6, f"Schema Present: {'Yes' if schema['has_schema'] else 'No'}", 0, 1)
            
            if schema['has_schema']:
                pdf.cell(0, 6, f"JSON-LD Scripts: {schema['json_ld_count']}", 0, 1)
                pdf.cell(0, 6, f"Microdata: {schema['microdata_count']}", 0, 1)
                if schema['schema_types']:
                    pdf.cell(0, 6, 'Schema Types:', 0, 1)
                    for schema_type in schema['schema_types'][:5]:  # Limit to 5 types
                        pdf.cell(0, 6, f"  - {schema_type}", 0, 1)
            pdf.ln(6)
            
            # PageSpeed Performance
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 8, 'PAGESPEED PERFORMANCE', 0, 1)
            pdf.set_font('Helvetica', '', 10)
            pdf.ln(2)
            
            if results['pagespeed_data']:
                ps = results['pagespeed_data']
                pdf.cell(0, 6, f"Performance Score: {ps['performance_score']}/100", 0, 1)
                pdf.cell(0, 6, f"First Contentful Paint: {ps['fcp']}", 0, 1)
            else:
                pdf.cell(0, 6, "PageSpeed data not available", 0, 1)
                pdf.cell(0, 6, "(API key not provided)", 0, 1)
            
            # Footer
            pdf.ln(15)
            pdf.set_font('Helvetica', 'I', 8)
            pdf.cell(0, 6, 'Generated by SEO Audit Tool | Sysdevcode', 0, 1, 'C')
            pdf.cell(0, 6, f"{results['audit_date']}", 0, 1, 'C')  
            
            # Add logo image at bottom center

            try:
                logo_path = "lo.png"  # Or your uploaded path: /mnt/data/89a5b77a-d21e-454f-8468-c17a034f4053.png
                logo_width = 65  # Adjust width as needed
                page_width = pdf.w  # A4 is 210mm
                x_position = (page_width - logo_width) / 2
                y_position = pdf.get_y() + 10

                if os.path.exists(logo_path):
                    pdf.image(logo_path, x=x_position, y=y_position, w=logo_width)
            except Exception as e:
                print(f"⚠️ Failed to load logo image: {e}")


            
            # Save PDF
            pdf.output(filename)
            return True
            
        except Exception as e:
            print(f"❌ PDF generation error: {str(e)}")
            return False

    def run(self):
        """Main application loop"""
        self.display_welcome()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Select an option (1-3): ").strip()
                
                if choice == '1':
                    self.get_api_key()
                elif choice == '2':
                    self.run_audit()
                elif choice == '3':
                    print("\n👋 Thank you for using SEO Audit Tool!")
                    print("Visit us again for more SEO analysis!")
                    break
                else:
                    print("❌ Invalid option. Please select 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {str(e)}")


def main():
    """Entry point of the application"""
    try:
        tool = SEOAuditTool()
        tool.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        print("Please check your Python environment and try again.")


if __name__ == "__main__":
    main()
