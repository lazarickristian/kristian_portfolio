from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from PIL import Image as PILImage
from reportlab.lib.colors import HexColor

custom_color = HexColor("#34b7a7")
custom_color_1 = HexColor("#0b8778")


def generate_pdf(club_name, club_logo_url, season, squad, fixtures, user):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    styles = getSampleStyleSheet()

    header_style = styles['Title']
    header_style.textColor = colors.black
    header_style.alignment = 1
    
    # Club Logo & Name
    if club_logo_url:
        elements.append(Image(club_logo_url))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"{club_name} '{season}' Season Report", header_style))
    elements.append(Spacer(1, 20))

    color_style = ParagraphStyle(name="Coloured", parent=styles["Normal"], textColor=custom_color_1) 
    squad_data = [
        ["SQUAD LIST", "", "", ""], ["Number", "Name", "Age", "Position"]
    ]  +[[player['Number'], Paragraph(f'<u><a href={player["Player_Link"]}>{player["Name"]}</a></u>'), player['Age'], player['Position']] for player in squad]
    
    squad_table = Table(squad_data, colWidths=[80, 175, 100, 155])
    squad_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),  # Merge first row across all columns
        ('BACKGROUND', (0, 0), (-1, 0), custom_color_1),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        ('BACKGROUND', (0, 1), (-1, 1), custom_color),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),

        ('BACKGROUND', (0, 2), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 2), (-1, -1), colors.black),

        ('ALIGN', (0, 2), (0, -1), 'CENTER'),  # Center align Number column
        ('ALIGN', (2, 2), (2, -1), 'CENTER'),  # Center align Age column

        ('GRID', (0, 0), (-1, -1), 1, colors.darkgray),
    ]))
    
    elements.append(squad_table)
    elements.append(PageBreak())

    #Fixtures
    fixtures_heading = [["FIXTURES"]]
    fixtures_heading_table = Table(fixtures_heading, colWidths=[510])
    fixtures_heading_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), custom_color_1),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ]))
    elements.append(fixtures_heading_table)
    elements.append(Spacer(1, 10))
    centered_style = ParagraphStyle(name="Centered", parent=styles["Normal"], alignment=1)
    for competition, matches in fixtures.items():
        fixture_data =  [[competition, "", ""]] + \
                        [["Date", "Opponent", "Result"]] + \
                        [[match['Date'], match['Opponent'], Paragraph(f'<u><a href={match["Result_Link"]}>{match["Result"]}</a></u>', centered_style)] for match in matches]  
              
        fixture_table = Table(fixture_data, colWidths=[170, 170, 170])
        fixture_table.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),  # Merge first row across all columns
            ('BACKGROUND', (0, 0), (-1, 0), custom_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

            ('GRID', (0, 0), (-1, -1), 1, colors.darkgray),
        ]))
        
        elements.append(fixture_table)
        elements.append(Spacer(1, 10))
    
    # Define a frame for the border
    def draw_border_add_footer_add_header(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.darkgrey)
        canvas.rect(15, 15, A4[0] - 30, A4[1] - 30)  # Creates a border around the page

        footer_text = "Data Source: Transfermarkt (https://www.transfermarkt.com/) | All rights reserved to the respective owners."
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(A4[0] / 2, 20, footer_text)  # Centered at the bottom of the page

        header_text = f"Report Generated By: {user} | Made By: Kristian Portfolio"
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(A4[0] / 2, A4[1]-25, header_text)  # Centered at the top of the page
        canvas.restoreState()

    pdf.build(elements, onFirstPage=draw_border_add_footer_add_header, onLaterPages=draw_border_add_footer_add_header)
    buffer.seek(0)
    
    # Save PDF locally for testing
    # with open("test_report.pdf", "wb") as f:
    #     f.write(buffer.getvalue())
    
    #print("PDF report generated: test_report.pdf")
    return buffer

