import os
import sys
import pandas as pd
from ..utils import get_foldername


class Tabela:
    def __init__(self):
        self.data_frame = None
        self.data_frame_informacoes = None
        self.data_frame_funcao = None
        self.path = None
        self.path_destino = None
        self.foldername = None

    def gerar_pasta_subpastas_cert(self):
        try:
            if not os.path.exists(self.path_destino + "/" + self.foldername):
                os.makedirs(self.path_destino + "/" + self.foldername)
            for i in self.data_frame_funcao.index.tolist():
                if not os.path.exists(
                    self.path_destino
                    + "/"
                    + self.foldername
                    + "/"
                    + self.data_frame_funcao["Função"][i]
                ):
                    os.makedirs(
                        self.path_destino
                        + "/"
                        + self.foldername
                        + "/"
                        + self.data_frame_funcao["Função"][i]
                    )
        except PermissionError:
            print(
                "Pasta para receber os certificados não escolhida, certificados não gerados!!!"
            )
            sys.exit()

    def set_data_frames(self, filepath):
        self.path = filepath
        self.foldername = get_foldername(self.path)
        try:
            self.data_frame = pd.read_excel(self.path)

            self.separar_tabela(self.data_frame)

            self.data_frame.dropna(axis=0, how="all", inplace=True)

            self.data_frame.drop_duplicates(keep="first", inplace=True)

            return True
        except ValueError:
            print(f"{self.path} - tabela vazia, " "certificados não gerados!!!")
            return False
        except KeyError:
            print(
                f'{self.path} - coluna "Informações" inexistente, '
                "certificados não gerados!!!"
            )
            return False

    def separar_tabela(self, data_frame):
        self.data_frame_informacoes = data_frame[["Informações"]].copy()
        self.data_frame_informacoes.dropna(axis=0, how="all", inplace=True)
        self.data_frame.drop(columns=["Informações"], inplace=True)
        self.data_frame_funcao = data_frame[["Função"]].copy()
        self.data_frame_funcao.dropna(axis=0, how="all", inplace=True)
        self.data_frame_funcao.drop_duplicates(keep="first", inplace=True)

    def get_data_frame(self):
        return self.data_frame

    def get_data_frame_informacoes(self):
        return self.data_frame_informacoes

    def verificar_tab_padrao(self, folder_destino):
        self.path_destino = folder_destino
        try:
            # pylint: disable=unused-variable
            dados_padrao = {  # noqa
                "nome_participante": self.data_frame["Nome"],
                "cpf_participante": self.data_frame["CPF"],
                "cargo_participante": self.data_frame["Função"],
                "frequencia_participante": self.data_frame["Frequência"],
                "nome_evento": self.data_frame_informacoes.iloc[0, 0],
                "carga_hor": self.data_frame_informacoes.iloc[1, 0],
                "nome_prof": self.data_frame_informacoes.iloc[2, 0],
                "nome_dep": self.data_frame_informacoes.iloc[3, 0],
                "data_inicial": self.data_frame_informacoes.iloc[4, 0],
                "data_final": self.data_frame_informacoes.iloc[5, 0],
                "nome_decano": self.data_frame_informacoes.iloc[6, 0],
            }
            # pylint: enable=unused-variable
            self.gerar_pasta_subpastas_cert()
            return True
        except KeyError:
            print(
                f'{self.path} - nem todos os campos da coluna " Informações "'
                "estão preenchidos, certificados não gerados!!!"
            )
            return False
        except IndexError:
            print(f"{self.path} - coluna está faltando, " "certificados não gerados!!!")
            return False
