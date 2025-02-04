# Import for the Desktop Bot
from botcity.core import DesktopBot, Backend

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

from botcity.core import DesktopBot
from pathlib import Path

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

class BotCityTask:
    def __init__(self):
        """
        Inicializa o bot, conectando ao Maestro e configurando o DesktopBot.
        """
        try:
            self._maestro = BotMaestroSDK.from_sys_args()
            self._bot = DesktopBot()
            self._execution = self._maestro.get_execution()
        except Exception as e:
            print(f"[Erro] Falha ao iniciar BotCityTask: {e}")
            self._execution = None

    def run(self):
        """
        Método principal para executar a automação.
        """
        try:
            self._log_task_details()
            self._aplication()  # Corrigido nome do método _aplication para _aplication
            self._finish_task()
        except Exception as e:
            self._handle_error(e)

    def _log_task_details(self):
        """
        Registra os detalhes da tarefa no console.
        """
        if not self._execution:
            print("[Erro] Nenhuma execução encontrada.")
            return

        print(f"[INFO] Task ID: {self._execution.task_id}")
        print(f"[INFO] Task Parameters: {self._execution.parameters}")

    def _aplication(self):  # Corrigido nome do método de _aplication para _aplication
        try:
            print("[INFO] Executando lógica do bot...")
            
            #COLOQUE AQUI O CAMINHO PARA O DIRETORIO DO PROGRAMA
            app_path = Path(r"C:\Program Files\Little Navmap\littlenavmap.exe")
            
            self._bot.execute(str(app_path))
            
            #COLOQUE AQUI O ID DA JANELA DO PROGRAMA
            aplication_id = "Name	Little Navmap 3.0.13.beta1 64-bit — MSFS 2020 / N 2501" 
            
            self._bot.connect_to_app(Backend.WIN_32, path=app_path, title=aplication_id)
                          
        except Exception as e:
            raise RuntimeError(f"[Erro] Falha na execução da lógica do bot: {e}")

    def _finish_task(self):
        """
        Marca a tarefa como concluída com sucesso no Maestro.
        """
        if not self._execution:
            print("[Erro] Não é possível finalizar a tarefa sem uma execução válida.")
            return

        try:
            self._maestro.finish_task(
                task_id=self._execution.task_id,
                status=AutomationTaskFinishStatus.SUCCESS,
                message="Task Finished OK.",
                total_items=1,
                processed_items=1,
                failed_items=0
            )
            print("[INFO] Tarefa finalizada com sucesso.")
        except Exception as e:
            print(f"[Erro] Falha ao finalizar a tarefa: {e}")

    def _handle_error(self, error):
        """
        Lida com erros ocorridos durante a execução.
        """
        print(f"[Erro] Ocorreu um erro: {error}")

        if self._execution:
            try:
                self._maestro.finish_task(
                    task_id=self._execution.task_id,
                    status=AutomationTaskFinishStatus.FAILED,
                    message=f"Task Failed: {error}",
                    total_items=0,
                    processed_items=0,
                    failed_items=1
                )
                print("[INFO] Tarefa marcada como falha no Maestro.")
            except Exception as e:
                print(f"[Erro] Falha ao reportar erro ao Maestro: {e}")

    @staticmethod
    def not_found(label):
        """
        Manipula casos em que um elemento não é encontrado.
        """
        print(f"[Aviso] Elemento não encontrado: {label}")

if __name__ == '__main__':
    bot_task = BotCityTask()
    bot_task.run()
