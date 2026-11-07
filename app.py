import streamlit as st
from datetime import date
from database import (
    init_db,
    create_demo_user, 
    get_applications, 
    add_application,
    update_application_status
)

st.set_page_config(
    page_title="CareerTrack",
    page_icon="💼",
    layout="wide"
)

#initialise the database
init_db()

#temporary development user
user_id = create_demo_user()

st.title("CareerTrack")
st.write("Your personal internship application tracker")

#Navigations
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard","My Applications", "Add Application"]
)

applications = get_applications(user_id)

#dashboard statistics
total_applications = len(applications)

interviews = sum (
    1 for app in applications
    if app["status"] == "Interview"
)

offers = sum(
    1 for app in applications
    if app["status"] == "Offer"
)

awaiting_response = sum(
    1 for app in applications
    if app["status"] == "Applied"
)

if page == "Dashboard":
    st.header("Your Application Overview")

    st.write(
        "Track your progress and stay on top of your opportunities"
    )

    #four metric cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Applications", total_applications)

    with col2:
        st.metric("In Interviews", interviews)

    with col3:
        st.metric("Offers", offers)
    
    with col4:
        st.metric("Awaiting Response", awaiting_response)

    st.divider()

    #recent applications
    st.subheader ("Recent Applications")

    recent_applications = applications[:5]

    if recent_applications:
        st.dataframe(
            recent_applications,
            hide_index=True,
            width="stretch"
        )
    else:
        st.info("No applications yet. Add your first application!")

elif page == "My Applications":

    st.subheader("My Applications")

    #search function

    search_query = st.text_input(
        "Search applications",
        placeholder="Search by company or role..."
    )

    filtered_applications = [
        app for app in applications
        if search_query.lower() in app["company"].lower()
        or search_query.lower() in app["role"].lower()
    ]

    if filtered_applications:
        st.dataframe(
            filtered_applications,
            hide_index=True,
            width="stretch"
        )
    else:
        st.info("No matching applications found.")

    if applications:
        st.dataframe(
            applications,
            width="stretch",
            hide_index = True
        )
    else:
        st.info("No applications yet. Add your first application!")

    status_filter = st.selectbox(
        "Filter by status",
        [
            "All",
            "Saved",
            "Applied",
            "Assessment",
            "Interview",
            "Offer",
            "Rejected"
        ]
    )

    if status_filter != "ALL":
        filtered_applications = [
            app for app in filtered_applications
            if app["status"] == status_filter
        ]

elif page == "Add Application":
    st.subheader("Add a New Application")

    with st.form("application_form"):

        company = st.text_input("Company name")
        role = st.text_input("Job title")

        status = st.selectbox(
            "Application status",
            [
                "Saved",
                "Applied",
                "Assessment",
                "Interview",
                "Offer",
                "Rejected"
            ],
            index = 1
        )

        date_applied = st.date_input(
            "Date applied",
            value = date.today()
        )
        
        job_url = st.text_input("Job listing URL (optional)")
        
        notes = st.text_area("Notes (optional)")
        
        submitted = st.form_submit_button(
            "Save Application",
            type="primary"
        )

    if submitted:
        if not company.strip() or not role.strip():
            st.error("Please enter both a company name and job title")

        else:
            application_id = add_application(
                user_id=user_id,
                company=company.strip(),
                role=role.strip(),
                status=status,
                date_applied=date_applied.isoformat(),
                job_url=job_url.strip(),
                notes=notes.strip()
            )

            st.success(
                f"Application #{application_id} saved successfully!"
            )

