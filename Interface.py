import customtkinter
import News_Scraper
import Model


class Interface:

    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.title("News Headline Analyser")
        self.root.geometry("600x600")

        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        bigHeading = customtkinter.CTkLabel(master=frame, text="News Headline Analyser", font=("Roboto", 26))
        bigHeading.pack(pady=20, padx=60)

        ## START TICKER ROW FRAME
        tickerRow = customtkinter.CTkFrame(master=frame, fg_color="transparent")
        tickerRow.pack(pady=10)

        inputLabel = customtkinter.CTkLabel(master=tickerRow, text="Enter stock ticker:", font=("Roboto", 16))
        inputLabel.pack(side="left", padx=(0, 8))

        self.tickerEntry = customtkinter.CTkEntry(master=tickerRow, width=120, font=("Roboto", 16))
        self.tickerEntry.pack(side="left")
        ## END TICKER ROW FRAME

        tickerSubmitButton = customtkinter.CTkButton(master=frame, text="Enter", font=("Roboto", 16), command=self.enterButtonClicked)
        tickerSubmitButton.pack(pady=10, padx=10)

        self.statusLabel = customtkinter.CTkLabel(master=frame, text="", font=("Roboto", 18))
        self.statusLabel.pack(pady=10, padx=10)

        ## START TABLE
        headerFrame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
        headerFrame.pack(padx=20, fill="x")
        headerFrame.grid_columnconfigure(0, weight=3)
        headerFrame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(
            master=headerFrame, text="Headline",
            font=("Roboto", 14, "bold"),
            fg_color="#1f538d", corner_radius=0
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 1))

        customtkinter.CTkLabel(
            master=headerFrame, text="Outcome",
            font=("Roboto", 14, "bold"),
            fg_color="#1f538d", corner_radius=0
        ).grid(row=0, column=1, sticky="nsew")

        self.scrollableTable = customtkinter.CTkScrollableFrame(master=frame)
        self.scrollableTable.pack(pady=(1, 10), padx=20, fill='both', expand=True)
        self.scrollableTable.grid_columnconfigure(0, weight=3)
        self.scrollableTable.grid_columnconfigure(1, weight=1)
        ## END TABLE

        self.root.mainloop()

    def populateTable(self, headlines):
        # Clear all existing rows
        for widget in self.scrollableTable.winfo_children():
            widget.destroy()

        # Repopulate with new data
        for i, (headline, outcome) in enumerate(headlines):
            row_color = "#2b2b2b" if i % 2 == 0 else "#1e1e1e"
            outcome_color = "#1a4a1a" if outcome == "Good" else "#4a1a1a"
            outcome_text_color = "#4caf50" if outcome == "Good" else "#f44336"

            customtkinter.CTkLabel(
                master=self.scrollableTable,
                text=headline,
                font=("Roboto", 13),
                fg_color=row_color,
                anchor="w",
                wraplength=380,
                corner_radius=0
            ).grid(row=i, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1), ipady=8)

            customtkinter.CTkLabel(
                master=self.scrollableTable,
                text=outcome,
                font=("Roboto", 13, "bold"),
                fg_color=outcome_color,
                text_color=outcome_text_color,
                anchor="center",
                corner_radius=0
            ).grid(row=i, column=1, sticky="nsew", pady=(0, 1), ipady=8)

    def enterButtonClicked(self):
        ticker = self.tickerEntry.get()
        if len(ticker) > 1 and len(ticker) < 5:

            scraper = News_Scraper.NewsScraper(ticker)
            status = scraper.retrieveNews()
            self.statusLabel.configure(text=status)

            if status == "Ticker not found":
                return

            headlines = scraper.returnNewsItems()
            if len(headlines) == 0:
                self.statusLabel.configure(text="No headlines found")
                return

            self.statusLabel.configure(text="Headlines found... Running AI analysis")
            model = Model.Model()
            outcome = model.predictHeadlines(headlines)

            if outcome != False:
                self.statusLabel.configure(text="Process complete")
                self.populateTable(outcome)