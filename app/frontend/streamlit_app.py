"""
Streamlit Frontend Application

Features:
- Learning Navigation Dashboard
- Resource Upload
- SQL Search
- Semantic Search
- Analytics
- DBMS Internals Demos
"""

import requests
import streamlit as st

# API Configuration
API_BASE_URL = "http://localhost:8000"


# Helper function to make API requests
def api_request(endpoint: str, method: str = "GET", data: dict | None = None):
    """Make API request to backend"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        else:
            return None

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


# Page: Learning Navigation
def show_learning_navigation():
    """Display learning navigation interface"""
    st.title("📚 Learning Navigation")
    st.write("Navigate through the 12-week CourseDB-AI learning curriculum")

    # Initialize curriculum button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Curriculum"):
            with st.spinner("Initializing curriculum..."):
                result = api_request("/learning/initialize", method="POST")
                if result:
                    st.success(
                        f"✅ Initialized {result['total_weeks']} weeks with {result['total_resources']} resources"
                    )

    # Get curriculum overview
    curriculum = api_request("/learning/curriculum")

    if not curriculum:
        st.warning("⚠️ Curriculum not initialized. Click 'Refresh Curriculum' to initialize.")
        return

    # Display progress
    st.metric(
        "Overall Progress",
        f"{curriculum['overall_progress']:.1f}%",
        f"{curriculum['completed_weeks']}/{curriculum['total_weeks']} weeks completed",
    )

    # Display weeks
    st.subheader("📅 12-Week Curriculum")

    # Week selector
    week_numbers = [w["week_number"] for w in curriculum["weeks"]]
    selected_week = st.selectbox(
        "Select Week",
        week_numbers,
        format_func=lambda x: f"Week {x}: {next((w['title'] for w in curriculum['weeks'] if w['week_number'] == x), '')}",
    )

    if selected_week:
        show_week_details(selected_week)

    # Display all weeks as cards
    st.subheader("All Weeks")
    for i in range(0, len(curriculum["weeks"]), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(curriculum["weeks"]):
                week = curriculum["weeks"][i + j]
                with col:
                    status_emoji = {"completed": "✅", "in_progress": "🔄", "not_started": "⏸️"}
                    st.markdown(
                        f"### {status_emoji.get(week['status'], '📝')} Week {week['week_number']}"
                    )
                    st.write(f"**{week['title']}**")
                    st.caption(f"{len(week.get('resources', []))} resources")


def show_week_details(week_number: int):
    """Display detailed information about a specific week"""
    navigation = api_request(f"/learning/weeks/{week_number}")

    if not navigation:
        st.error("Failed to load week details")
        return

    current_week = navigation["current_week"]

    st.markdown("---")
    st.header(f"Week {current_week['week_number']}: {current_week['title']}")

    # Status badge
    status_colors = {"completed": "green", "in_progress": "orange", "not_started": "gray"}
    status = current_week["status"]
    st.markdown(
        f"**Status:** :{status_colors.get(status, 'blue')}[{status.replace('_', ' ').title()}]"
    )

    # Description
    if current_week.get("description"):
        st.info(current_week["description"])

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if navigation.get("previous_week"):
            if st.button("⬅️ Previous Week"):
                st.session_state.selected_week = navigation["previous_week"]["week_number"]
                st.rerun()

    with col3:
        if navigation.get("next_week"):
            if st.button("Next Week ➡️"):
                st.session_state.selected_week = navigation["next_week"]["week_number"]
                st.rerun()

    # Resources
    st.subheader("📁 Learning Resources")
    resources = current_week.get("resources", [])

    if not resources:
        st.warning("No resources found for this week")
    else:
        # Group resources by type
        resource_types = {}
        for resource in resources:
            rtype = resource["resource_type"]
            if rtype not in resource_types:
                resource_types[rtype] = []
            resource_types[rtype].append(resource)

        # Display by type
        type_icons = {
            "documentation": "📄",
            "exercise": "✏️",
            "solution": "✅",
            "notebook": "📓",
            "code": "💻",
            "reflection": "🤔",
        }

        for rtype, items in sorted(resource_types.items()):
            with st.expander(f"{type_icons.get(rtype, '📎')} {rtype.title()} ({len(items)})"):
                for resource in items:
                    st.markdown(f"- **{resource['title']}**")
                    st.caption(f"📂 `{resource['file_path']}`")

    # Update status
    st.subheader("Update Status")
    new_status = st.selectbox(
        "Change week status",
        ["not_started", "in_progress", "completed"],
        index=["not_started", "in_progress", "completed"].index(current_week["status"]),
    )

    if st.button("💾 Save Status"):
        result = api_request(
            f"/learning/weeks/{week_number}/status", method="PUT", data={"status": new_status}
        )
        if result:
            st.success(f"✅ Status updated to: {new_status}")
            st.rerun()


# Page: Search Resources
def show_search_resources():
    """Search for learning resources"""
    st.title("🔍 Search Learning Resources")

    query = st.text_input("Search resources", placeholder="Enter keywords...")

    resource_type = st.selectbox(
        "Filter by type (optional)",
        ["All", "documentation", "exercise", "solution", "notebook", "code", "reflection"],
    )

    if st.button("Search") and query:
        params = {"query": query}
        if resource_type != "All":
            params["resource_type"] = resource_type

        results = api_request("/learning/search", data=params)

        if results:
            st.success(f"Found {len(results)} resources")
            for result in results:
                with st.expander(f"📄 {result['title']}"):
                    st.write(f"**Type:** {result['resource_type']}")
                    st.write(f"**Path:** `{result['file_path']}`")
        else:
            st.warning("No results found")


# Page: Statistics
def show_statistics():
    """Display curriculum statistics"""
    st.title("📊 Curriculum Statistics")

    stats = api_request("/learning/stats")

    if stats:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Weeks", stats["total_weeks"])
            st.metric("Total Resources", stats["total_resources"])

        with col2:
            st.subheader("Weeks by Status")
            for status, count in stats.get("weeks_by_status", {}).items():
                st.write(f"**{status.replace('_', ' ').title()}:** {count}")

        st.subheader("Resources by Type")
        for rtype, count in stats.get("resources_by_type", {}).items():
            st.write(f"**{rtype.title()}:** {count}")


# Main app
def main():
    st.set_page_config(page_title="CourseDB-AI Learning System", page_icon="📚", layout="wide")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Learning Navigation", "Search Resources", "Statistics"])

    # Display selected page
    if page == "Learning Navigation":
        show_learning_navigation()
    elif page == "Search Resources":
        show_search_resources()
    elif page == "Statistics":
        show_statistics()


if __name__ == "__main__":
    main()
