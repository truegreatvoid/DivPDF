import PySimpleGUI as sg
import os
import PyPDF2

def split_pdf(input_pdf, output_dir, max_pages_per_pdf):
    pdf = PyPDF2.PdfReader(input_pdf)

    if len(pdf.pages) == 0:
        sg.popup_error("O PDF está vazio.")
        return

    base_filename = os.path.splitext(os.path.basename(input_pdf))[0]

    num_parts = (len(pdf.pages) + max_pages_per_pdf - 1) // max_pages_per_pdf

    for part in range(num_parts):
        start_page = part * max_pages_per_pdf
        end_page = min((part + 1) * max_pages_per_pdf, len(pdf.pages))

        output_pdf = PyPDF2.PdfWriter()
        for page_num in range(start_page, end_page):
            output_pdf.add_page(pdf.pages[page_num])

        output_filename = os.path.join(output_dir, f"{base_filename} parte {part + 1}.pdf")
        with open(output_filename, "wb") as output_file:
            output_pdf.write(output_file)

        print(f"Criado: {output_filename}")

    sg.popup("Concluído!", f"Os arquivos foram salvos em {output_dir}")

def main():
    sg.theme("LightBlue")

    layout = [
        [sg.Text("Escolha o arquivo PDF:", size=(26, 1)), sg.InputText(key="input_pdf", size=(40, 1)), sg.FileBrowse("Diretório")],
        [sg.Text("Escolha o diretório de saída:", size=(26, 1)), sg.InputText(key="output_dir", size=(40, 1)), sg.FolderBrowse("Diretório")],
        [sg.Text("Quantidade de páginas por PDF:", size=(26, 1)), sg.InputText(key="max_pages_per_pdf", size=(5, 1))],
        [sg.Button("Dividir PDF", size=(20, 1))],
    ]

    window = sg.Window("Divisor de PDF", layout, resizable=False, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Dividir PDF":
            input_pdf = values["input_pdf"]
            output_dir = values["output_dir"]

            max_pages_per_pdf_entry = values["max_pages_per_pdf"]
            if max_pages_per_pdf_entry.isdigit():
                max_pages_per_pdf = int(max_pages_per_pdf_entry)
            else:
                sg.popup_error("Por favor, insira um valor numérico para a quantidade de páginas por PDF.")
                continue
            
            if not input_pdf or not output_dir:
                sg.popup_error("Por favor, escolha o arquivo PDF e o diretório de saída.")
            else:
                split_pdf(input_pdf, output_dir, max_pages_per_pdf)

    window.close()

if __name__ == "__main__":
    main()
