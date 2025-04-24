from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation

def add_margin_to_pdf(input_pdf_path, output_pdf_path, margin_size=20):
    """
    给 PDF 增加页边距
    :param input_pdf_path: 输入的 PDF 文件路径
    :param output_pdf_path: 输出的 PDF 文件路径
    :param margin_size: 额外增加的边距（单位：points）
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        # 获取原页面大小
        original_width = page.mediabox.width
        original_height = page.mediabox.height
        
        # 创建一个新的空白 PDF 页面
        new_width = original_width + 2 * margin_size
        new_height = original_height + 2 * margin_size
        new_page = PageObject.create_blank_page(width=new_width, height=new_height)

        # 计算缩放比例，使内容适应新页面
        scale_x = original_width / new_width
        scale_y = original_height / new_height
        scale_factor = min(scale_x, scale_y)  # 选择最小比例，确保内容不超出边界
        
        # 应用缩放和平移变换
        transformation = (
            Transformation()
            .scale(scale_factor)  # 适应新页面
            # .translate(margin_size, margin_size)  # 移动到正确的位置            
            .translate(margin_size*2, margin_size*2)  # 移动到正确的位置
        )
        # page.add_transformation(Transformation().translate(margin_size, margin_size))
        page.add_transformation(transformation)
        
        # 合并原页面到新页面
        new_page.merge_page(page, expand=True)

        # 添加到输出 PDF
        writer.add_page(new_page)

    # 保存新的 PDF
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

# 示例使用
input_pdf = "3.pdf"  # 你的输入文件
output_pdf = "3_with_margin.pdf"  # 你的输出文件
add_margin_to_pdf(input_pdf, output_pdf, margin_size=50)
