import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
import pandas as pd
from groupme_analytics import run_analytics  # Import your analytics functions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import networkx as nx
import random
import plotly.graph_objects as go
import webbrowser

# Set the theme for the customtkinter widgets
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

# Global variable to store the data DataFrame. I did this to avoid 
global excluded_users
excluded_users = {'GroupMe Calendar', 'Zo', 'system'}

# Function to generate a random color
def get_random_color():
    """
    Generate a random color in hexadecimal format.

    Returns:
    - str: A string representing the color in hexadecimal format.
    """
    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return random_color

# Function to create a color palette for the users
def generate_color_palette(users):
    """
    Generate a color palette mapping each user to a unique color.
    
    Parameters:
    - users: list or iterable, a list of unique user names
    
    Returns:
    - dict: A dictionary mapping user names to color codes
    """
    color_palette = {user: get_random_color() for user in users}
    return color_palette

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.current_canvas = None

        # Function to open a file dialog and load the file
        def load_file():
            global data_df
            global file_path
            global likes_df
            file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "message.json")])
            if file_path:
                try:
                    data_df, likes_df = run_analytics(file_path, excluded_users)
                    run_all()
                    #display_data(data_df)
                except Exception as e:
                    messagebox.showerror("Error", str(e))        
        
        # Function to open the URL
        def open_groupme_export():
            webbrowser.open('https://web.groupme.com/profile/export')

        def run_all():
            #destroy_all_graphs()
            create_combined_likes_graph()
            create_combined_likes_graph
            create_combined_activity_graph()
            create_combined_swear_graph()
            create_name_changes_graph()
            create_lexical_diversity_graph()
            create_message_amount_graph()
            create_message_length_graph()
            create_fav_relationship_graph()
            show_achievements()
            
        def destroy_all_graphs():
            # Assuming self.main_frame is where all your graphs are packed or gridded
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # If you have other frames or tabs where graphs are placed, you can do the same:
            # for widget in some_other_frame.winfo_children():
            #     widget.destroy()

            # Reset references to None if you're keeping track of them
            self.current_canvas = None
            # create tabview
            self.main_frame = ctk.CTkTabview(self, width=250)
            self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            self.main_frame.add("Count")
            self.main_frame.add("Length")
            self.main_frame.add("Cussing")
            self.main_frame.add("Likes")
            self.main_frame.add("Activity")
            self.main_frame.add("Name Changes")
            self.main_frame.add("Lexical Diversity")
            self.main_frame.add("Favorites")
            self.main_frame.add("Achievements")
            self.main_frame.tab("Count").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.main_frame.tab("Length").grid_columnconfigure(0, weight=1)

        def create_combined_swear_graph():
            if data_df is not None and 'Swear_Count' in data_df.columns and '%_Swear' in data_df.columns:
                # Create a new window (Toplevel widget) for the graph
                cuss_tab = self.main_frame.tab("Cussing")

                # Configure the grid layout for the favorites tab
                cuss_tab.grid_columnconfigure(0, weight=1)
                cuss_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax1 = plt.subplots()

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')
                ax1.set_facecolor('#2b2b2b')

                # Set the positions for the bars
                indices = np.arange(len(data_df))
                width = 0.35  # Width of the bars

                # Plotting Swear Count bars
                ax1.bar(indices - width/2, data_df['Swear_Count'], width, label='Swear Count', color='darkblue')

                # Setting labels, title, and ticks for the primary y-axis
                ax1.set_xlabel('User', color='white')
                ax1.set_ylabel('Swear Count', color='blue')
                ax1.set_title('Swear Count and Percentage per User', color='white')
                ax1.set_xticks(indices)
                ax1.set_xticklabels(data_df.index, rotation=45, color='white')
                ax1.tick_params(axis='y', labelcolor='blue')

                # Creating a secondary y-axis for the percentage
                ax2 = ax1.twinx()
                ax2.bar(indices + width/2, data_df['%_Swear'], width, label='% Swear Words', color='darkgreen')
                ax2.set_ylabel('% Swear Words', color='darkgreen')
                ax2.tick_params(axis='y', labelcolor='darkgreen')
                ax2.set_ylim(0, 3)  # Setting the y-axis limit for percentage up to 3%

                # Adjusting legend text color for visibility
                legend = fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
                for text in legend.get_texts():
                    text.set_color('white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=cuss_tab)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

                # Store the current canvas for later use
                self.current_canvas = canvas

        # Function to create a combined bar graph for likes given and likes taken
        def create_combined_likes_graph():
            if data_df is not None and 'Likes_Given' in data_df.columns and 'Likes_Taken' in data_df.columns:
                # Create a new window (Toplevel widget) for the graph
                likes_tab = self.main_frame.tab("Likes")
                
                # Configure the grid layout for the favorites tab
                likes_tab.grid_columnconfigure(0, weight=1)
                likes_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Set the positions for the bars
                indices = np.arange(len(data_df))
                width = 0.35  # Width of the bars

                # Plotting both bars
                ax.bar(indices - width/2, data_df['Likes_Given'], width, label='Likes Given', color='darkblue')
                ax.bar(indices + width/2, data_df['Likes_Taken'], width, label='Likes Taken', color='darkgreen')

                # Adding labels and title
                ax.set_xlabel('User')
                ax.set_ylabel('Likes Count')
                ax.set_title('Likes Given and Taken per User')
                ax.set_xticks(indices)
                ax.set_xticklabels(data_df.index, rotation=45)
                ax.legend()
                

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=likes_tab)  
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a combined bar graph for Early Bird and Night Owl percentages
        def create_combined_activity_graph():
            if data_df is not None and 'Early_Bird' in data_df.columns and 'Night_Owl' in data_df.columns:
                # Create a new window (Toplevel widget) for the graph
                time_tab = self.main_frame.tab("Activity")
                
                # Configure the grid layout for the favorites tab
                time_tab.grid_columnconfigure(0, weight=1)
                time_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()

                # Set the positions for the bars
                indices = np.arange(len(data_df))
                width = 0.35  # Width of the bars

                # Plotting both bars
                ax.bar(indices - width/2, data_df['Early_Bird'], width, label='6AM-8AM Activity', color='orange')
                ax.bar(indices + width/2, data_df['Night_Owl'], width, label='2AM-4AM Activity', color='purple')

                # Adding labels and title
                ax.set_xlabel('User')
                ax.set_ylabel('Percentage')
                ax.set_title('Early Bird and Night Owl Activity per User')
                ax.set_xticks(indices)
                ax.set_xticklabels(data_df.index, rotation=45)
                ax.legend()
                
                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=time_tab)  
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a bar graph for name changes
        def create_name_changes_graph():
            if data_df is not None and 'Name_Change' in data_df.columns:
                name_tab = self.main_frame.tab("Name Changes")
                
                # Configure the grid layout for the favorites tab
                name_tab.grid_columnconfigure(0, weight=1)
                name_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()

                # Plotting the bar graph
                data_df['Name_Change'].plot(kind='bar', ax=ax, color='teal')
                ax.set_title("Name Changes per User")
                ax.set_xlabel("User")
                ax.set_ylabel("Number of Name Changes")

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=name_tab)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a bar graph for lexical diversity
        def create_lexical_diversity_graph():
            if data_df is not None and 'Lex_Div' in data_df.columns:
                lex_tab = self.main_frame.tab("Lexical Diversity")
                
                # Configure the grid layout for the favorites tab
                lex_tab.grid_columnconfigure(0, weight=1)
                lex_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()

                # Plotting the bar graph
                data_df['Lex_Div'].plot(kind='bar', ax=ax, color='violet')
                ax.set_title("Lexical Diversity per User")
                ax.set_xlabel("User")
                ax.set_ylabel("Lexical Diversity Score")

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=lex_tab)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a bar graph for message count
        def create_message_amount_graph():
            if data_df is not None and 'Mess_Count' in data_df.columns:
                message_tab = self.main_frame.tab("Count")
                
                # Configure the grid layout for the favorites tab
                message_tab.grid_columnconfigure(0, weight=1)
                message_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()
                
                # Identify the highest and lowest values
                max_value = data_df["Mess_Count"].max()
                min_value = data_df["Mess_Count"].min()

                # Assign colors based on the value
                colors = ['red' if value == max_value else 'blue' if value == min_value else 'gray' for value in data_df["Mess_Count"]]

                # Plotting the bar graph
                data_df['Mess_Count'].plot(kind='bar', ax=ax, color=colors)
                ax.set_title("Message Count per User")
                ax.set_xlabel("User")
                ax.set_ylabel("Message Count")

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=message_tab)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a bar graph for average message length
        def create_message_length_graph():
            if data_df is not None and 'Avg_Mess_Len' in data_df.columns:
                message_tab = self.main_frame.tab("Length")
                
                # Configure the grid layout for the favorites tab
                message_tab.grid_columnconfigure(0, weight=1)
                message_tab.grid_rowconfigure(0, weight=1)

                # Create the figure for the plot
                fig, ax = plt.subplots()
                
                # Identify the highest and lowest values
                max_value = data_df["Avg_Mess_Len"].max()
                min_value = data_df["Avg_Mess_Len"].min()

                # Assign colors based on the value
                colors = ['red' if value == max_value else 'blue' if value == min_value else 'gray' for value in data_df["Avg_Mess_Len"]]

                # Plotting the bar graph
                data_df['Avg_Mess_Len'].plot(kind='bar', ax=ax, color=colors)
                ax.set_title("Average Message Length per User")
                ax.set_xlabel("User")
                ax.set_ylabel("Average Message Length")

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')  # Change 'lightgray' to your desired background color for the figure
                ax.set_facecolor('#2b2b2b')  # Change 'whitesmoke' to your desired background color for the axes
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=message_tab)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # Function to create a network graph for the "Fav" relationships
        def create_fav_relationship_graph():
            if data_df is not None and 'Fav' in data_df.columns:
                favorites_tab = self.main_frame.tab("Favorites")

                # Configure the grid layout for the favorites tab
                favorites_tab.grid_columnconfigure(0, weight=1)
                favorites_tab.grid_rowconfigure(0, weight=1)

                # Create the matplotlib figure
                fig, ax = plt.subplots()


                # You might also want to change text color to something lighter for visibility
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                

                # Creating a directed graph
                G = nx.DiGraph()

                # Adding nodes and edges based on the "Fav" relationships
                for user, fav_user in data_df['Fav'].items():
                    G.add_edge(user, fav_user)

                # Drawing the graph
                pos = nx.spring_layout(G)  # positions for all nodes
                nx.draw(G, pos, with_labels=True, node_color='darkblue', 
                        node_size=1500, edge_color='gray', linewidths=1, 
                        font_size=10, ax=ax, font_color='white')  # Set font_color to 'white'

                # No need for x, y labels in a network graph
                ax.set_title("Favorite User Relationships", color='white')  # Set title color to white

                # Embed the plot in the Tkinter window
                canvas = FigureCanvasTkAgg(fig, master=favorites_tab)
                canvas.draw()  # Draw the canvas before packing
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(row=0, column=0, sticky='nsew')  # Use grid here

                # Set the background color
                fig.patch.set_facecolor('#2b2b2b')
                ax.set_facecolor('#2b2b2b')

        # Function to create a Sankey diagram for the "Fav" relationships
        def create_sankey():
            # Define nodes
            title = "Likes Flow"
            all_nodes = likes_df['Sender'].tolist() + likes_df['Receiver'].tolist()
            nodes = list(set(all_nodes))
            nodes.sort()  # Sort the nodes if needed
            node_indices = {node: i for i, node in enumerate(nodes)}

            # Define links
            source_indices = [node_indices[sender] for sender in likes_df['Sender']]
            target_indices = [node_indices[receiver] for receiver in likes_df['Receiver']]
            values = likes_df['Likes'].tolist()

            # Create Sankey diagram
            fig = go.Figure(data=[go.Sankey(
                node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes),
                link=dict(source=source_indices, target=target_indices, value=values)
            )])

            fig.update_layout(title_text=title, font_size=10)
            fig.show()

        # Function to calculate and show achievements
        def show_achievements():
            if data_df is not None:
                # Convert columns to numeric and handle NaN values
                numeric_columns = ['Mess_Count', 'Avg_Mess_Len', '%_Swear', 'Likes_Given', 'Likes_Taken', 'Early_Bird', 'Night_Owl', 'Name_Change', 'Lex_Div']
                for col in numeric_columns:
                    data_df[col] = pd.to_numeric(data_df[col], errors='coerce').fillna(0)

                achievements = {
                    "Shut Up": data_df['Mess_Count'].idxmax(),
                    "We Miss You": data_df['Mess_Count'].idxmin(),
                    "Long Winded": data_df['Avg_Mess_Len'].idxmax(),
                    "Concise": data_df['Avg_Mess_Len'].idxmin(),
                    "Potty Mouth": data_df['%_Swear'].idxmax(),
                    "Angel": data_df['%_Swear'].idxmin(),
                    "Big Love": data_df['Likes_Given'].idxmax(),
                    "Favorite Child": data_df['Likes_Taken'].idxmax(),
                    "Piece of Shit": (data_df['Likes_Taken'] - data_df['Likes_Given']).idxmax(),
                    "Early Bird": data_df['Early_Bird'].idxmax(),
                    "Night Owl": data_df['Night_Owl'].idxmax(),
                    "Identity Crisis": data_df['Name_Change'].idxmax(),
                    "Know Yourself": data_df['Name_Change'].idxmin(),
                    "Big Brain": data_df['Lex_Div'].idxmax(),
                    "Wurdz R hard": data_df['Lex_Div'].idxmin(),
                }

                # Define achievements with descriptions and emojis
                achievement_descriptions = {
                    "Shut Up": ("User with the highest overall sent messages", "🗣️"),
                    "We Miss You": ("User with the least amount of sent messages", "👻"),
                    "Long Winded": ("User with the highest average message length", "📜"),
                    "Concise": ("User with the lowest average message length", "✂️"),
                    "Potty Mouth": ("User with the highest average swear percentage", "🤬"),
                    "Angel": ("User with the lowest average swear percentage", "😇"),
                    "Big Love": ("User who has given the most likes", "💖"),
                    "Favorite Child": ("User who has received the most likes", "🌟"),
                    "Piece of Shit": ("User who has the largest number of likes taken over given", "💩"),
                    "Early Bird": ("User with the highest 6AM - 8AM activity", "🐦"),
                    "Night Owl": ("User with the highest 2AM - 4AM activity", "🦉"),
                    "Identity Crisis": ("User who has changed their name the most", "🔀"),
                    "Know Yourself": ("User who has changed their name the least", "🤔"),
                    "Big Brain": ("User with the highest lexical diversity", "🧠"),
                    "Wurdz R hard": ("User with the lowest lexical diversity", "🤷")
                }

                # Create a new customtkinter window (Toplevel widget) for the achievements
                #achievement_window = ctk.CTkToplevel(self.main_frame)
                #achievement_window.title("Achievements")
                #achievement_window.geometry("1200x400")  # Adjust the size as needed
                #achievement_window.attributes("-topmost", True)

                 # Get the frame of the "Achievements" tab
                achievements_tab = self.main_frame.tab("Achievements")

                # Frame to hold the achievements in a grid, now a child of the achievements tab
                grid_frame = ctk.CTkFrame(achievements_tab)
                grid_frame.grid(row=0, column=0, sticky="nsew")
                achievements_tab.grid_columnconfigure(0, weight=1)
                achievements_tab.grid_rowconfigure(0, weight=1)

                # Set up grid layout
                num_columns = 3
                grid_frame.grid_columnconfigure(tuple(range(num_columns)), weight=1)
                for i in range(15):  # Adjust the range based on the number of rows needed
                    grid_frame.grid_rowconfigure(i, weight=1)

                # Display each achievement with emoji, name, and description in a grid
                for i, (achievement, (desc, emoji)) in enumerate(achievement_descriptions.items()):
                    row, col = divmod(i, num_columns)
                    user = achievements.get(achievement, "N/A")

                    # Achievement title with emoji
                    achievement_label = ctk.CTkLabel(grid_frame, text=f"{emoji} {achievement}", font=("Arial", 24, "bold"))
                    achievement_label.grid(row=row*3, column=col, padx=10, pady=10, sticky="nsew")

                    # Achievement recipient's name
                    name_label = ctk.CTkLabel(grid_frame, text=f"{user}", font=("Arial", 14))
                    name_label.grid(row=row*3+1, column=col, padx=10, pady=5, sticky="nsew")

                    # Achievement description
                    desc_label = ctk.CTkLabel(grid_frame, text=f"{desc}", font=("Arial", 12))
                    desc_label.grid(row=row*3+2, column=col, padx=10, pady=5, sticky="nsew")

        # Function to open a window to exclude users
        def open_exclusion_window():
            exclusion_window = ctk.CTkToplevel(self.main_frame)
            exclusion_window.title("Exclude Users")
            exclusion_window.attributes("-topmost", True)
            exclusion_window.geometry("200x500")

            # Check if data_df exists and has user data
            if 'data_df' in globals() and not data_df.empty:
                users = set(data_df.index) - excluded_users  # Exclude already excluded users
            else:
                #tk.messagebox.showerror("Error", "No user data available.")
                return

            # Creating a Scrollable Frame to display checkboxes
            scrollable_frame = ctk.CTkScrollableFrame(exclusion_window)
            scrollable_frame.pack(fill="both", expand=True)

            checkboxes = {}
            for user in sorted(users):
                checkboxes[user] = ctk.CTkCheckBox(master=scrollable_frame, text=user)
                checkboxes[user].pack(pady=2, padx=20, anchor="w")

            def add_to_exclusions():
                for user, checkbox in checkboxes.items():
                    if checkbox.get() == 1:  # Check if the checkbox is selected
                        excluded_users.add(user)
                # Re-run analytics with updated exclusions
                # (Ensure file_path is a global variable)
                global data_df
                global likes_df
                data_df, likes_df = run_analytics(file_path, excluded_users)
                exclusion_window.destroy()
                destroy_all_graphs()
                run_all()

            add_button = ctk.CTkButton(exclusion_window, text="Add to Exclusions", command=add_to_exclusions)
            add_button.pack(pady=10)

        self.iconbitmap('./data/groupme.ico')  # If you have an .ico file
        # or
        
        # Configure window
        self.title("GroupMetrics")
        self.geometry("1600x875")

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        # Button sizes
        button_width = 145
        button_height = 30


        # Frame for the logo labels
        logo_frame = ctk.CTkFrame(self.sidebar_frame)
        logo_frame.pack(pady=10)

        # Spacer frame to push buttons to the bottom
        spacer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#2b2b2b")
        spacer_frame.pack(side="top", fill="both", expand=True)

        # Labels for different parts of the title
        ctk.CTkLabel(logo_frame, text="Group", font=ctk.CTkFont(size=25, weight="bold"), fg_color="#2b2b2b", text_color="white").pack(side="left")
        ctk.CTkLabel(logo_frame, text="Me", font=ctk.CTkFont(size=25, weight="bold"), fg_color="#2b2b2b", text_color="#206cf8").pack(side="left")
        ctk.CTkLabel(logo_frame, text="trics", font=ctk.CTkFont(size=25, weight="bold"), fg_color="#2b2b2b", text_color="orange").pack(side="left")  # Replace YOUR_CHOSEN_COLOR with the desired color

        # Load file button
        load_button = ctk.CTkButton(
            self.sidebar_frame, text="Load JSON File", command=load_file,
            fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
            width=button_width, height=button_height
        )
        load_button.pack(side="bottom", pady=10)

        # Button to open GroupMe export page
        export_button = ctk.CTkButton(
            self.sidebar_frame, text="Get JSON File", command=open_groupme_export,
            width=button_width, height=button_height
        )
        export_button.pack(side="bottom", pady=10)

        # Exclude users button
        exclude_users_button = ctk.CTkButton(
            self.sidebar_frame, text="Exclude Users", command=open_exclusion_window,
            width=button_width, height=button_height
        )
        exclude_users_button.pack(side="bottom", pady=10)

        # Button to show achievements
        achievements_button = ctk.CTkButton(
            self.sidebar_frame, text="Clear Graphs", command=destroy_all_graphs,
            width=button_width, height=button_height
        )
        achievements_button.pack(side="bottom", pady=10)

        # Button to show the "Fav" relationship graph
        fav_relationship_graph_button = ctk.CTkButton(
            self.sidebar_frame, text="Detailed Likes", command=create_sankey,
            width=button_width, height=button_height
        )
        fav_relationship_graph_button.pack(side="bottom", pady=10)

        # Main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create tabview
        self.main_frame = ctk.CTkTabview(self, width=250)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.add("Count")
        self.main_frame.add("Length")
        self.main_frame.add("Cussing")
        self.main_frame.add("Likes")
        self.main_frame.add("Activity")
        self.main_frame.add("Name Changes")
        self.main_frame.add("Lexical Diversity")
        self.main_frame.add("Favorites")
        self.main_frame.add("Achievements")
        self.main_frame.tab("Count").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.main_frame.tab("Length").grid_columnconfigure(0, weight=1)
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
