import flet as ft
import pdf2image, pypdf, ocrmypdf
import numpy as np
import base64, re
from io import BytesIO
from PIL import Image as PILImage


class CustomRow(ft.Row):
    def __init__(self, fixedString, leftButton_click, rightButton_click, variableString=""):
        super().__init__()
        self.leftButton = ft.IconButton(icon=ft.icons.ARROW_CIRCLE_LEFT, icon_size = 35, tooltip='Go to previous page', on_click=leftButton_click)
        self.rightButton = ft.IconButton(icon=ft.icons.ARROW_CIRCLE_RIGHT, icon_size = 35, tooltip='Go to next page', on_click = rightButton_click)
        self.fixedText = ft.Text(value=fixedString)
        self.variableText = ft.Text(value=variableString)
        self.controls = [self.leftButton, self.variableText, ft.Text(value="/"), self.fixedText, self.rightButton]   
        self.alignment = ft.MainAxisAlignment.CENTER  


class PdfManager:
    def __init__(self):
        pass


    def ConvertPDFIntoImage64(self, filename: str, pageNum: int=None, imageFormat: str ="JPEG"):
        '''
        Converts a pdf file into a list of 64-bit images. If a page number is not specified, all pages of the pdf are converted.  

        Parameters:
                        filename (str): The name of the pdf file. Use the absolute path (path + name).
                        pageNum (int): The number of the page to be converted. Default is None: all pages are converted.
                        imageFormat (str): The format of the converted images. Default is JPEG. 

        Returns:
                        images64 (list): List of 64-bit images.
        '''
        if pageNum is None:
            pilObjects= pdf2image.convert_from_path(filename, use_pdftocairo=False)
        else:
            # Convert_From_Path works with base-1 indexes. Returns always a list
            pilObjects= pdf2image.convert_from_path(filename, first_page=pageNum+1, 
                    last_page=pageNum+1, use_pdftocairo=False)

        images64 = []
        for pilObject in pilObjects:
            pil_img = PILImage.fromarray(np.asarray(pilObject))
            buff = BytesIO()
            pil_img.save(buff, format=imageFormat)
            pic = base64.b64encode(buff.getvalue()).decode("utf-8")
            images64.append(pic)
        return images64


    def FindStrIntoPDF(self, reader: pypdf.PdfReader, keyword: str, pages_and_indices : bool= False):
        '''
        Finds a keyword into a pdf file. Returns alternatevely the pages or the pages and indices in which the keyword was found.  

        Parameters:
                        reader (pypdf.PdfReader): A pdf file reader
                        keyword (str): The keyword to be searched into pdf file
                        pages_and_indices (bool): True to return pages and indices of search. Default is false.

        Returns:
                        results (list): List of integers corresponding to pages or list of dictionaries corresponding to pages and indices. Empty if keyword was not found. 
        '''
        results = []

        if pages_and_indices:
            for index, page in enumerate(reader.pages):
                text = page.extract_text() 
                text_lower = text.lower()

                res_search = [m.start() for m in re.finditer(keyword.lower(), text_lower)]
                if len(res_search)>0:
                    page_occurrences = {'pages': index, 'indexes': res_search}
                    results.append(page_occurrences)
        else:        
            for index, page in enumerate(reader.pages):
                text = page.extract_text() 
                text_lower = text.lower()

                res_search = text_lower.find(keyword.lower())
                if res_search >= 0:
                    results.append(index)

        return results


    def ConvertIntegerListIntoStringInterval(self, pages: list):
        '''
        Convert a list of integers into a string that represent page intervals or single pages. Three consecutive pages are considered as page intervals. Empty if the list is empty.  

        Parameters:
                        pages (list): List of integers corresponding to pages numbers.

        Returns:
                         (str): String in the format "19-22, 25"
        '''
        if len(pages) == 0:  # empty case
            return ''

        result = []
        def _process(first, last):
            if first != last:  # range, but handle consecutive case
                result.append(f"{first}{'-' if last - first > 1 else ', '}{last}")
            else:
                result.append(str(first))  # first==last, single number

        first = last = pages[0]  # initialize range tracking to first number
        for page in pages[1:]:  # iterate remaining numbers
            if page <= last:  # input not increasing
                raise ValueError('Not consecutive numbers. Try to sort the list.')
            if page == last + 1:  # next number is consecutive
                last = page
            else:
                _process(first, last)  # next number not consecutive
                first = last = page    # reset for next range
        _process(first, last)  # no more numbers, finish last range

        return ', '.join(result)


    def ConvertStringIntervalIntoIntegerList(self, searchResult: str):
        '''
        Converts a string that represent page intervals or single pages comma-separated into a list of integers.  

        Parameters:
                        searchResult (str): The string to be converted

        Returns:
                         (list): List of integers corresponding to pages. Empty if string is empty. 
        '''
        if searchResult == "":
            return []
        else:
            # find comma indices; a comma is added to manage the case of a single num
            commas = [match.start() for match in re.finditer(',', searchResult + ",")]

            subparts = []
            if len(commas) > 0:
                start = 0
                for index, val in enumerate(commas):
                    #print("INDEX: ", index, "VAL: ", val)
                    sliceString = searchResult[start : val]
                    sliceString = sliceString.strip()
                    start = val+1

                    # find hyphen indices
                    hyphen = [match.start() for match in re.finditer('-', sliceString)] 

                    if len(hyphen) > 0:
                        leftNum = int(sliceString[: hyphen[0]].strip())
                        rightNum = int(sliceString[hyphen[0] + 1 : ].strip()) 
                        
                        subparts.append(list(range(leftNum, rightNum+1)))
                    else:
                        # intervals.append(int(part))
                        subparts.append([int(sliceString)])

                return [x for xs in subparts for x in xs]


def main(page: ft.Page):
    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            global pdfFullname, pdfLen, currentPage, reader

            pdfFullname = ", ".join(map(lambda f: f.path, e.files))

            currentPage = 0            
            viewer = pdfManager.ConvertPDFIntoImage64(pdfFullname, pageNum = currentPage)
            reader = pypdf.PdfReader(pdfFullname)
            pdfLen = len(reader.pages)

            contImg.content = ft.Image(src_base64 = viewer[0], fit=ft.ImageFit.FILL,)
            displayPageNum.variableText.value = str(currentPage+1)
            displayPageNum.fixedText.value = str(pdfLen)
            tf_PageNum.max_length = len(str(pdfLen))
            expPanel2.content.disabled = False
            button_RunOCR.disabled = False
            page.update()     


    def Go_To_Page(e):
        global pdfFullname, pdfLen, currentPage

        pageNum = int(e.control.value)
        if pageNum >= 1 and pageNum <= pdfLen:
            currentPage = pageNum -1

            viewer = pdfManager.ConvertPDFIntoImage64(pdfFullname, pageNum = currentPage)
            contImg.content = ft.Image(src_base64 = viewer[0], fit=ft.ImageFit.FILL,)
            displayPageNum.variableText.value = str(currentPage+1)
            e.control.value = ""
            page.update()


    def Go_To_Previous_Page(e):
        global pdfFullname, currentPage

        if currentPage > 0:
            currentPage -= 1
            
            viewer = pdfManager.ConvertPDFIntoImage64(pdfFullname, pageNum = currentPage)
            contImg.content = ft.Image(src_base64 = viewer[0], fit=ft.ImageFit.FILL,)
            displayPageNum.variableText.value = str(currentPage+1)
            page.update()


    def Go_To_Next_Page(e):
        global pdfFullname, pdfLen, currentPage

        if currentPage < pdfLen - 1:
            currentPage += 1

            viewer = pdfManager.ConvertPDFIntoImage64(pdfFullname, pageNum = currentPage)
            contImg.content = ft.Image(src_base64 = viewer[0], fit=ft.ImageFit.FILL,)
            displayPageNum.variableText.value = str(currentPage+1)
            page.update()


    def Search_String_Into_Pdf(e):
        global reader

        keyword = e.control.value

        dlg = ft.AlertDialog(title=ft.Text("PROCESSING...", text_align="CENTER"),
                content=ft.ProgressRing(height=50, width=50, stroke_width=4),
            )
        page.dialog = dlg
        dlg.open = True
        page.update()

        pages = pdfManager.FindStrIntoPDF(reader = reader, keyword = keyword)
        tf_ExtractPdfPages.value = pdfManager.ConvertIntegerListIntoStringInterval([page + 1 for page in pages])

        page.close_dialog()
        page.update()


    def Extract_Pdf_Pages(e):
        global reader, pdfFullname

        pages = e.control.value
        if len(pages) > 0:
            dlg = ft.AlertDialog(title=ft.Text("PROCESSING...", text_align="CENTER"),
                content=ft.ProgressRing(height=50, width=50, stroke_width=4),
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

            intervals = pdfManager.ConvertStringIntervalIntoIntegerList(pages)
            intervals.sort()

            writer = pypdf.PdfWriter()
            for interval in intervals:
                writer.add_page(reader.pages[interval-1])

            # PDF WRITING
            output_fullname = pdfFullname[: -4] + "_extracted.pdf"
            with open(output_fullname, "wb") as output_stream:
                writer.write(output_stream)

                page.close_dialog()
                page.snack_bar = ft.SnackBar(ft.Text(output_fullname + " SAVED !"))
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Please insert the number of pages to extract."))
            page.snack_bar.open = True
            page.update()



    def Extract_Pdf_Pages_Focus(e):
        stringMsg = "Insert comma-separated values for single pages (4, 11, 21). Insert hyphen-separated values for intervals of pages. (10-19)"

        page.snack_bar = ft.SnackBar(ft.Text(stringMsg))
        page.snack_bar.open = True
        page.update()


    def Run_OCR(e):
        global pdfFullname

        output_fullname = pdfFullname[: -4] + "_ocr.pdf"
        with open(output_fullname, "wb") as output_stream:
            dlg = ft.AlertDialog(title=ft.Text("PROCESSING...", text_align="CENTER"),
                content=ft.ProgressRing(height=50, width=50, stroke_width=4),
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

            ocrmypdf.ocr(pdfFullname, output_stream, force_ocr=True, output_type='pdf')

            page.close_dialog()
            page.update()

            page.snack_bar = ft.SnackBar(ft.Text(output_fullname + " SAVED !"))
            page.snack_bar.open = True
            page.update()


    
    pdfManager = PdfManager()

    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    page.overlay.extend([pick_file_dialog])
    button_PickFile = ft.ElevatedButton(text="Select a PDF file", icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_file_dialog.pick_files(allow_multiple=False, allowed_extensions=["pdf"],),
        tooltip="Select a PDF file",)

    displayPageNum = CustomRow(fixedString="", leftButton_click=Go_To_Previous_Page, rightButton_click=Go_To_Next_Page)

    tf_PageNum = ft.TextField(label="Go to page", hint_text="Page Number", width=140, height=65, border_color="white", keyboard_type=ft.KeyboardType.NUMBER, on_submit=Go_To_Page)  

    expPanel1 = ft.ExpansionPanel(bgcolor=ft.colors.BLUE_400, header=ft.ListTile(title=ft.Text("VIEW")),
                content= ft.Column([button_PickFile, displayPageNum, tf_PageNum], 
                                horizontal_alignment = "center", alignment = "center",), )  


    tf_SearchString = ft.TextField(label="Find all occurrencies", hint_text="Enter the key to be searched", width=350, height=65, border_color="white", icon = ft.icons.SEARCH, on_submit=Search_String_Into_Pdf)

    tf_ExtractPdfPages= ft.TextField(label="Insert number of pages to extract", hint_text="Comma or Hyphen separated", width=350, height=65, keyboard_type=ft.KeyboardType.NUMBER, border_color="white", icon = ft.icons.DOWNLOAD, on_submit=Extract_Pdf_Pages, on_focus=Extract_Pdf_Pages_Focus)

    expPanel2 = ft.ExpansionPanel(bgcolor=ft.colors.BLUE_400, header=ft.ListTile(title=ft.Text("FIND & EXTRACT")),
                content = ft.Column([tf_SearchString, tf_ExtractPdfPages], horizontal_alignment = "center", alignment = "center", disabled = True),  )


    button_RunOCR = ft.ElevatedButton(text="Run OCR on PDF file", icon=ft.icons.UPLOAD_FILE,
        on_click=Run_OCR,
        disabled = True,
        tooltip="Apply Object Character Recognition to a PDF File",)


    expPanel3 = ft.ExpansionPanel(bgcolor=ft.colors.BLUE_400, 
                                header=ft.ListTile(title=ft.Text("CONVERT")),
                                content = ft.Container(content=ft.Column([button_RunOCR], 
                                                horizontal_alignment = "center", 
                                                alignment = "center",
                                                spacing=50,),
                                padding = ft.padding.only(bottom=20)),  
                )

    expPanList = ft.ExpansionPanelList(elevation=10, controls=[expPanel1, expPanel2, expPanel3],)


    contLeft = ft.Container(height = page.height, width = 0.3 * page.width,
        border=ft.border.all(3, ft.colors.RED),)

    contRight = ft.Container(height = page.height, width = 0.7 * page.width,
        border=ft.border.all(3, ft.colors.RED),)

    contImg = ft.Container(height = contRight.height * 0.9, width = contRight.width * 0.4,
        #bgcolor = ft.colors.BROWN,
        )

    contLeft.content = expPanList
    contRight.content = ft.Column([contImg], horizontal_alignment = "center", alignment = "center")

    page.add(ft.Row([contLeft, contRight]))
    #page.window_height = 400
    #page.window_width = 800
    #page.adaptive = True #adaptive to different platforms
    page.window_maximized = True
    page.scroll = ft.ScrollMode.AUTO
    page.title = "PDF SUITE"
    page.update()

ft.app(target=main, assets_dir="assets")
