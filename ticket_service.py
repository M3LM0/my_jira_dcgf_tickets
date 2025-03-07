import os
import json
import pandas as pd

class TicketService:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.file_path = self.config.get("excel_path", "suivi_jira_dcgf.xlsx")
        self.columns = ["N°", "Nom", "Programme", "Description", "Statut", "Priorité"]
        self.load_tickets()

    def load_tickets(self):
        if os.path.exists(self.file_path):
            try:
                self.df = pd.read_excel(self.file_path, engine='openpyxl')
            except Exception as e:
                print("Erreur lors du chargement du fichier :", e)
                self.df = pd.DataFrame(columns=self.columns)
        else:
            self.df = pd.DataFrame(columns=self.columns)
            self.save_tickets()

    def save_tickets(self):
        try:
            self.df.to_excel(self.file_path, index=False, engine='openpyxl')
        except Exception as e:
            print("Erreur lors de la sauvegarde du fichier :", e)

    def add_ticket(self, nom, programme, description, statut, priorite):
        if self.df.empty:
            next_num = 1
        else:
            try:
                next_num = int(self.df["N°"].max()) + 1
            except Exception:
                next_num = 1

        new_ticket = {
            "N°": next_num,
            "Nom": nom,
            "Programme": programme,
            "Description": description,
            "Statut": statut,
            "Priorité": priorite
        }

        new_ticket_df = pd.DataFrame([new_ticket])
        self.df = pd.concat([self.df, new_ticket_df], ignore_index=True)
        self.save_tickets()

    def delete_ticket(self, ticket_number):
        self.df = self.df[self.df["N°"] != ticket_number]
        self.save_tickets()

    def update_ticket(self, ticket_number, nom, programme, description, statut, priorite):
        idx = self.df.index[self.df["N°"] == ticket_number]
        if not idx.empty:
            self.df.loc[idx, "Nom"] = nom
            self.df.loc[idx, "Programme"] = programme
            self.df.loc[idx, "Description"] = description
            self.df.loc[idx, "Statut"] = statut
            self.df.loc[idx, "Priorité"] = priorite
            self.save_tickets()