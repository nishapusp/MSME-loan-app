import streamlit as st
from database import Database
from utils import colorful_document_upload
from document_extraction import extract_data_from_document, map_extracted_data_to_form_fields
from sections import (
    basic_information_section,
    proprietor_partners_directors_section,
    credit_facilities_section,
    collateral_and_guarantor_section,
    past_performance_and_business_relations_section,
    associate_concerns_and_statutory_obligations_section,
    undertakings_and_document_upload_section,
    review_section
)

# Initialize database
db = Database()

# Page config
st.set_page_config(
    layout="wide", 
    page_title="MSME Loan Application",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0
    if 'application_id' not in st.session_state:
        st.session_state.application_id = None
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    if 'documents' not in st.session_state:
        st.session_state.documents = {}

def auto_fill_field(key, value, source):
    """Auto-fill form fields and track the source"""
    if value and (key not in st.session_state or not st.session_state[key]):
        st.session_state[key] = value
        st.session_state[f"{key}_source"] = source
        # Update form_data in session state
        st.session_state.form_data[key] = value

def create_input_field(label, key, value="", help=""):
    """Create input field and track changes"""
    input_value = st.text_input(
        label, 
        value=st.session_state.get(key, value), 
        key=key, 
        help=help
    )
    # Update form_data in session state
    if input_value:
        st.session_state.form_data[key] = input_value
    return input_value

def save_application_data():
    """Save all application data to database"""
    try:
        application_data = {
            'basic_info': {
                'enterprise_name': st.session_state.get('enterprise_name'),
                'udyam_number': st.session_state.get('udyam_number'),
                'classification': st.session_state.get('classification'),
                'date_of_classification': st.session_state.get('date_of_classification'),
                'social_category': st.session_state.get('social_category'),
                'address': st.session_state.get('address'),
                'state': st.session_state.get('state'),
                'major_activity': st.session_state.get('major_activity'),
                'nic_5_digit': st.session_state.get('nic_5_digit'),
                'mobile': st.session_state.get('mobile'),
                'email': st.session_state.get('email'),
                'date_of_incorporation': st.session_state.get('date_of_incorporation'),
                'date_of_commencement': st.session_state.get('date_of_commencement'),
                'gst_number': st.session_state.get('gst_number'),
                'pan': st.session_state.get('pan'),
                'constitution': st.session_state.get('constitution')
            },
            'directors': [
                {
                    'name': st.session_state.get(f'director_name_{i}'),
                    'designation': st.session_state.get(f'director_designation_{i}'),
                    'dob': st.session_state.get(f'director_dob_{i}'),
                    'pan': st.session_state.get(f'director_pan_{i}'),
                    'aadhaar': st.session_state.get(f'director_aadhaar_{i}'),
                    'address': st.session_state.get(f'director_address_{i}'),
                    'mobile': st.session_state.get(f'director_mobile_{i}'),
                    'networth': st.session_state.get(f'director_networth_{i}')
                }
                for i in range(st.session_state.get('num_directors', 1))
            ],
            'credit_facilities': {
                'existing': [
                    {
                        'type': st.session_state.get(f'existing_facility_type_{i}'),
                        'limit': st.session_state.get(f'existing_facility_limit_{i}'),
                        'outstanding': st.session_state.get(f'existing_facility_outstanding_{i}'),
                        'bank': st.session_state.get(f'existing_facility_bank_{i}'),
                        'security': st.session_state.get(f'existing_facility_security_{i}')
                    }
                    for i in range(st.session_state.get('num_facilities', 0))
                ],
                'proposed': [
                    {
                        'type': st.session_state.get(f'proposed_facility_type_{i}'),
                        'amount': st.session_state.get(f'proposed_facility_amount_{i}'),
                        'purpose': st.session_state.get(f'proposed_facility_purpose_{i}'),
                        'security': st.session_state.get(f'proposed_facility_security_{i}')
                    }
                    for i in range(st.session_state.get('num_proposed_facilities', 1))
                ]
            },
            'collateral': [
                {
                    'owner': st.session_state.get(f'collateral_owner_{i}'),
                    'type': st.session_state.get(f'collateral_type_{i}'),
                    'details': st.session_state.get(f'collateral_details_{i}'),
                    'value': st.session_state.get(f'collateral_value_{i}')
                }
                for i in range(st.session_state.get('num_collaterals', 0))
            ],
            'performance': {
                'past_performance': {
                    year: {
                        'net_sales': st.session_state.get(f'Net Sales_{year}'),
                        'net_profit': st.session_state.get(f'Net Profit_{year}'),
                        'capital': st.session_state.get(f'Capital_{year}')
                    }
                    for year in ["Past Year-II", "Past Year-I", "Present Year", "Next Year"]
                }
            },
            'business_relations': {
                'suppliers': [
                    {
                        'name': st.session_state.get(f'supplier_name_{i}'),
                        'contact': st.session_state.get(f'supplier_contact_{i}'),
                        'association': st.session_state.get(f'supplier_association_{i}'),
                        'business_percentage': st.session_state.get(f'supplier_business_{i}')
                    }
                    for i in range(st.session_state.get('num_suppliers', 3))
                ],
                'customers': [
                    {
                        'name': st.session_state.get(f'customer_name_{i}'),
                        'contact': st.session_state.get(f'customer_contact_{i}'),
                        'association': st.session_state.get(f'customer_association_{i}'),
                        'business_percentage': st.session_state.get(f'customer_business_{i}')
                    }
                    for i in range(st.session_state.get('num_customers', 3))
                ]
            },
            'undertakings': [
                st.session_state.get(f'undertaking_{i}')
                for i in range(8)  # Assuming 8 undertakings as per the form
            ],
            'documents': st.session_state.get('documents', {})
        }

        if st.session_state.application_id:
            result = db.update_application(st.session_state.application_id, application_data)
        else:
            result = db.save_application(application_data)
            st.session_state.application_id = result.inserted_id
        
        return True
    except Exception as e:
        st.error(f"Error saving application: {str(e)}")
        return False

def main():
    initialize_session_state()

    st.title("MSME Loan Application")

    # Define sections
    sections = [
        ("Basic Information", basic_information_section),
        ("Proprietor/Partners/Directors", proprietor_partners_directors_section),
        ("Credit Facilities", credit_facilities_section),
        ("Collateral and Guarantors", collateral_and_guarantor_section),
        ("Past Performance and Business Relations", past_performance_and_business_relations_section),
        ("Associate Concerns and Statutory Obligations", associate_concerns_and_statutory_obligations_section),
        ("Undertakings and Document Upload", undertakings_and_document_upload_section),
        ("Review Application", review_section)
    ]

    # Create tabs
    tabs = st.tabs([section[0] for section in sections])

    # Display current section
    for i, (section_name, section_function) in enumerate(sections):
        with tabs[i]:
            section_function(
                auto_fill_field=auto_fill_field,
                create_input_field=create_input_field,
                colorful_document_upload=colorful_document_upload,
                extract_data_from_document=extract_data_from_document
            )

    # Navigation and Progress
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Previous") and st.session_state.current_tab > 0:
            st.session_state.current_tab -= 1
            save_application_data()  # Save before navigation
            st.experimental_rerun()
            
    with col2:
        # Progress indicator
        progress = (st.session_state.current_tab + 1) / len(sections)
        st.progress(progress)
        st.write(f"Section {st.session_state.current_tab + 1} of {len(sections)}")

    with col3:
        if st.session_state.current_tab < len(sections) - 1:
            if st.button("Next"):
                save_application_data()  # Save before navigation
                st.session_state.current_tab += 1
                st.experimental_rerun()
        else:
            if st.button("Submit Application"):
                if save_application_data():
                    st.success("Application submitted successfully!")
                    st.write(f"Your application ID is: {st.session_state.application_id}")
                    # You might want to send an email confirmation or generate a PDF here
                else:
                    st.error("Error submitting application. Please try again.")

    # Save progress on form changes
    if st.session_state.form_data:
        save_application_data()

if __name__ == "__main__":
    main()