import streamlit as st
import pandas as pd
import pylightxl as xl

def checkdatatype(datatype):
    if datatype.lower() == "int":
        return("integer")
    elif datatype.lower() == "str":
        return("string")
    elif datatype.lower() == "date":
        return("date")
    elif datatype.lower() == "char":
        return("char")
    else:
        return(datatype+" is not datatpye")

# set tab title
st.set_page_config(page_title="Ferdy Streamlit", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

# set the title of page
st.title("""
Generate Query Insert MySQL
""")

st.sidebar.markdown("""

<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css"
        integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>

<body>
    <p style='text-align: center;' class="author">CREATED BY FERDYHAPE</p>
    <p style='text-align: center;'>Connect with me!</p>
    <div class="group-icon" style="text-align: center; font-size: 35px">
        <a href="https://github.com/ferdyhape"><i class="fa-brands fa-github"></i></a>
        <a href="https://instagram.com/ferdyhape"><i class="fa-brands fa-instagram"></i></a>
        <a href="https://www.linkedin.com/in/ferdy-hahan-pradana/"><i class="fa-brands fa-linkedin"></i></a>
    </div>
    <style>
    .group-icon {
        margin-top: 20px;
        padding: 5px 5px;
        border-radius: 25px;
        background-color: #F6F6F6;
    } 
    .group-icon:hover {
        background-color: #F9F9F9;
    }
    .fa-github {
        color: #333;
    }
    .fa-instagram {
        color: #833AB4;
    }
    .fa-linkedin {
        color: #0e76a8;
    }
    .author {
        margin: 0px 10px;;
        font-size: 20px;
        font-weight: bold;
    }
    p {
        margin: 0px 10px;;
    }
    a {
        margin: 0 10px;
    }
    </style>
</body>

""", unsafe_allow_html=True)

#initiate and refresh the list 
atribute_datatype_list = []
atribute_datatype_list.clear()

column_address_list = []
column_address_list.clear()

atribute_name_list = []
atribute_name_list.clear()

atribute_datatype_list = []
atribute_datatype_list.clear()

# list of input
table_name = st.text_input("Input table name: ")
input_atribute_name = st.text_input("Enter the Name of attribute sequentially (separated by comma): ")
input_atribute_datatype = st.text_input("Enter the data type of attribute sequentially (separated by comma): ")
input_column_address = st.text_input("Enter the address of the value column sequentially (separated by comma): ")
sheet_name = st.text_input("Sheet name: ")
range_rows = st.number_input("Range rows until: ", 0)
excel_uploader = st.file_uploader("Upload Excel Source", 'xlsx')
first_row_header = st.checkbox("First Row is Header")

# process for input address of the value column in list variable
input_column_address = input_column_address.upper()
input_column_address = input_column_address.replace(" ", "")
column_address_list = input_column_address.split(",")

# process for input attribute name in list variable
input_atribute_name = input_atribute_name.replace(" ", "")
atribute_name_list = input_atribute_name.split(",")

# process for input attribute data type in list variable
input_atribute_datatype = input_atribute_datatype.replace(" ", "")
atribute_datatype_list = input_atribute_datatype.split(",")

# variable for spesific attribute name table
name_for_query = ', '.join(atribute_name_list)

# if first row is header
start_row = 0
row_addr = 1
if first_row_header:
    start_row = 1
    row_addr = 2

#create generate button
generate = st.button("Generate")


dump_address_list = []

# if generate button clicked
if generate:
    st.write("""
    Table Structure
    """)

    excel_file = xl.readxl(excel_uploader)
    d = {'Name': atribute_name_list, 'Datatype': atribute_datatype_list, 'Address Column': column_address_list}
    df = pd.DataFrame(data=d)
    st.table(df)

    st.write("""
    Query
    """)

    st.text(f"""
            INSERT INTO {table_name} ({name_for_query}) 
            VALUES
            """)

    for i in range (start_row, range_rows+1):
        j = 0
        dump_address_list.clear()
        for col_address in column_address_list:
            dump = column_address_list[j]+str(row_addr)
            value = str(excel_file.ws(ws=sheet_name).address(address=dump))
            if value.isdigit():
                dump_address_list.append(value)
            else:
                dump_address_list.append(f'"{value}"')
            j+=1
        query = ', '.join(dump_address_list)
        st.text(f"({query}),")
        row_addr+=1
    