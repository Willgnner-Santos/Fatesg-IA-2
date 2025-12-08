"""
Cliente de API para integração com o backend CogniKids
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional
import json

class APIClient:
    """Cliente para comunicação com o backend Flask"""
    
    def __init__(self, base_url: str = "http://localhost:5001/api"):
        """
        Inicializa o cliente da API
        
        Args:
            base_url (str): URL base da API
        """
        self.base_url = base_url
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Retorna headers com token de autenticação se disponível
        
        Returns:
            dict: Headers HTTP
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Adiciona token JWT se disponível
        if 'token' in st.session_state:
            headers['Authorization'] = f"Bearer {st.session_state['token']}"
        
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Trata a resposta da API
        
        Args:
            response: Objeto Response do requests
            
        Returns:
            dict: Dados da resposta ou erro
        """
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"error": "Resposta inválida do servidor"}
        
        if response.status_code >= 400:
            return {
                "success": False,
                "error": data.get("message", data.get("error", "Erro desconhecido")),
                "status_code": response.status_code
            }
        
        return {
            "success": True,
            "data": data,
            "status_code": response.status_code
        }
    
    # ==================== AUTENTICAÇÃO ====================
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza login na API
        
        Args:
            email (str): Email do usuário
            password (str): Senha
            
        Returns:
            dict: Resposta com token e dados do usuário
        """
        try:
            response = self.session.post(
                f"{self.base_url}/login",
                json={"email": email, "senha": password},
                headers=self._get_headers(),
                timeout=10
            )
            result = self._handle_response(response)
            
            # Salva token na sessão se login bem-sucedido
            if result.get("success") and "token" in result.get("data", {}):
                st.session_state['token'] = result['data']['token']
            
            return result
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Não foi possível conectar ao servidor. Verifique se o backend está rodando."
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Tempo de conexão esgotado. Tente novamente."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao fazer login: {str(e)}"
            }
    
    def register(self, nome: str, email: str, password: str, tipo: str, **kwargs) -> Dict[str, Any]:
        """
        Registra novo usuário
        
        Args:
            nome (str): Nome completo
            email (str): Email
            password (str): Senha
            tipo (str): Tipo de usuário (aluno, professor, pai/responsável)
            **kwargs: Dados adicionais (data_nascimento, etc)
            
        Returns:
            dict: Resposta do registro
        """
        try:
            payload = {
                "nome": nome,
                "email": email,
                "senha": password,
                "tipo": tipo,
                **kwargs
            }
            
            response = self.session.post(
                f"{self.base_url}/register",
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao registrar: {str(e)}"
            }
    
    # ==================== ALUNOS ====================
    
    def get_student_profile(self, student_id: str) -> Dict[str, Any]:
        """
        Obtém perfil do aluno
        
        Args:
            student_id (str): ID do aluno
            
        Returns:
            dict: Dados do aluno
        """
        try:
            response = self.session.get(
                f"{self.base_url}/students/{student_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_student_grades(self, student_id: str) -> Dict[str, Any]:
        """
        Obtém notas do aluno
        
        Args:
            student_id (str): ID do aluno
            
        Returns:
            dict: Notas e desempenho
        """
        try:
            response = self.session.get(
                f"{self.base_url}/grades/student/{student_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_student_challenges(self, student_id: str) -> Dict[str, Any]:
        """
        Obtém desafios/atividades do aluno
        
        Args:
            student_id (str): ID do aluno
            
        Returns:
            dict: Lista de desafios
        """
        try:
            response = self.session.get(
                f"{self.base_url}/challenges/student/{student_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== PROFESSORES (TEACHERS) ====================
    
    def get_teacher_students(self, teacher_id: str) -> Dict[str, Any]:
        """
        Obtém a lista de alunos de um professor específico.
        
        Args:
            teacher_id (str): ID do professor logado
            
        Returns:
            dict: Resposta da API com a lista de alunos
        """
        try:
            # Esta rota está em cognikids-backend/app/Controllers/teacher_controller.py
            response = self.session.get(
                f"{self.base_url}/teachers/{teacher_id}/students",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar alunos: {str(e)}"}
    
    def get_student_feelings(self, student_id: str) -> Dict[str, Any]:
        """
        Busca os sentimentos de um aluno específico (rota do professor).
        GET /api/teachers/students/<student_id>/feelings
        """
        try:
            # Esta rota vem do teacher_controller.py
            response = self.session.get(
                f"{self.base_url}/teachers/students/{student_id}/feelings",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar sentimentos: {str(e)}"}
    
    def get_crisis_alerts(self) -> Dict[str, Any]:
        """
        Verifica alertas de crise em tempo real para os alunos do professor.
        GET /api/teachers/crisis_alerts
        """
        try:
            # Esta rota foi criada no teacher_controller.py
            response = self.session.get(
                f"{self.base_url}/teachers/crisis_alerts",
                headers=self._get_headers(),
                timeout=10 # Timeout de 10 segundos
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar alertas: {str(e)}"}
    
    def get_student_alert_history(self, student_id: str) -> Dict[str, Any]:
        """
        Busca o historico de alertas de crise de um aluno especifico.
        Retorna os ultimos 30 dias de alertas.
        GET /api/teachers/students/<student_id>/alert_history
        
        Args:
            student_id (str): ID do aluno
            
        Returns:
            dict: Historico de alertas com data, severidade, BPM, GSR, movement_score, motivo
        """
        try:
            response = self.session.get(
                f"{self.base_url}/teachers/students/{student_id}/alert_history",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar histórico de alertas: {str(e)}"}
    
    def get_students_average_grade(self) -> Dict[str, Any]:
        """
        Busca a média de notas de todos os alunos do professor.
        GET /api/teachers/students_average_grade
        """
        try:
            response = self.session.get(
                f"{self.base_url}/teachers/students_average_grade",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar média de notas: {str(e)}"}
    
    # ==================== ATIVIDADES/DESAFIOS ====================
    
    def get_challenges(self, theme: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista desafios disponíveis
        
        Args:
            theme (str, optional): Filtrar por tema
            
        Returns:
            dict: Lista de desafios
        """
        try:
            params = {"theme": theme} if theme else {}
            response = self.session.get(
                f"{self.base_url}/challenges",
                params=params,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def submit_challenge_response(self, challenge_id: str, student_id: str, 
                                   answers: list, score: int, time_spent: float) -> Dict[str, Any]:
        """
        Envia resposta de um desafio
        
        Args:
            challenge_id (str): ID do desafio
            student_id (str): ID do aluno
            answers (list): Lista de respostas
            score (int): Pontuação obtida
            time_spent (float): Tempo gasto em segundos
            
        Returns:
            dict: Confirmação do envio
        """
        try:
            payload = {
                "challenge_id": challenge_id,
                "student_id": student_id,
                "answers": answers,
                "score": score,
                "time_spent": time_spent
            }
            
            response = self.session.post(
                f"{self.base_url}/challenges/submit",
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== NOTAS E DESEMPENHO ====================
    
    def save_grade(self, student_id: str, subject: str, grade: float, 
                   observation: Optional[str] = None) -> Dict[str, Any]:
        """
        Salva nota do aluno
        
        Args:
            student_id (str): ID do aluno
            subject (str): Matéria/tema
            grade (float): Nota
            observation (str, optional): Observações
            
        Returns:
            dict: Confirmação
        """
        try:
            payload = {
                "student_id": student_id,
                "subject": subject,
                "grade": grade,
                "observation": observation
            }
            
            response = self.session.post(
                f"{self.base_url}/grades",
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== DADOS IoT ====================
    
    def get_iot_data(self, student_id: str, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém dados biométricos IoT do aluno
        
        Args:
            student_id (str): ID do aluno
            start_date (str, optional): Data inicial (YYYY-MM-DD)
            end_date (str, optional): Data final (YYYY-MM-DD)
            
        Returns:
            dict: Dados biométricos
        """
        try:
            params = {}
            if start_date:
                params['start_date'] = start_date
            if end_date:
                params['end_date'] = end_date
            
            response = self.session.get(
                f"{self.base_url}/iot/student/{student_id}",
                params=params,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== GERENCIAMENTO (PROFESSOR) ====================
    
    def update_student(self, student_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza os dados de um aluno (rota de professor)
        PUT /api/students/<student_id>
        """
        try:
            response = self.session.put(
                f"{self.base_url}/students/{student_id}",
                json=data,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao atualizar aluno: {str(e)}"}

    def delete_student(self, student_id: str) -> Dict[str, Any]:
        """
        Remove um aluno (rota de professor)
        DELETE /api/students/<student_id>
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/students/{student_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao remover aluno: {str(e)}"}

    def get_teacher_classes(self) -> Dict[str, Any]:
        """
        Busca as turmas do professor logado.
        GET /api/classes
        """
        try:
            url = f"{self.base_url}/classes"
            headers = self._get_headers()
            
            print(f"[DEBUG get_teacher_classes] URL: {url}")
            print(f"[DEBUG get_teacher_classes] Headers: {headers}")
            
            # O backend (class_controller.py) já filtra automaticamente
            # as turmas com base no token do professor.
            response = self.session.get(url, headers=headers, timeout=10)
            
            print(f"[DEBUG get_teacher_classes] Status code: {response.status_code}")
            print(f"[DEBUG get_teacher_classes] Response text: {response.text[:500]}")
            
            result = self._handle_response(response)
            print(f"[DEBUG get_teacher_classes] Result: {result}")
            
            return result
        except Exception as e:
            print(f"[DEBUG get_teacher_classes] ERRO: Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"Erro ao buscar turmas: {str(e)}"}

    def create_student(self, nome: str, email: str, senha: str, turma_id: str) -> Dict[str, Any]:
        """
        Cria um novo aluno (rota de professor)
        POST /api/students
        """
        try:
            payload = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "turma_id": turma_id
            }
            response = self.session.post(
                f"{self.base_url}/students",
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao criar aluno: {str(e)}"}

    def create_class(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova turma (rota de professor)
        POST /api/classes/classes
        """
        try:
            # O backend (class_controller.py) espera:
            # name, grade, section, school_year
            payload = {
                "name": data.get("nome"),
                "grade": data.get("grade"),
                "section": data.get("section"), # Período (Manhã, Tarde)
                "school_year": data.get("school_year")
            }
            response = self.session.post(
                f"{self.base_url}/classes/classes",
                json=payload,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao criar turma: {str(e)}"}

    def get_class_details(self, class_id: str) -> Dict[str, Any]:
        """
        Busca os detalhes de uma turma específica.
        GET /api/classes/classes/<class_id>
        Nota: URL duplicado devido ao url_prefix='/api/classes' no backend
        """
        try:
            response = self.session.get(
                f"{self.base_url}/classes/classes/{class_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar detalhes da turma: {str(e)}"}
    
    def update_class(self, class_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza uma turma existente
        PUT /api/classes/classes/<class_id>
        """
        try:
            response = self.session.put(
                f"{self.base_url}/classes/classes/{class_id}",
                json=data,
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao atualizar turma: {str(e)}"}
    
    def delete_class(self, class_id: str) -> Dict[str, Any]:
        """
        Desativa uma turma (soft delete)
        DELETE /api/classes/classes/<class_id>
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/classes/classes/{class_id}",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao excluir turma: {str(e)}"}

    def enroll_student_in_class(self, class_id: str, student_id: str) -> Dict[str, Any]:
        """
        Matricula um aluno em uma turma.
        POST /api/classes/<class_id>/enroll_student
        """
        try:
            response = self.session.post(
                f"{self.base_url}/classes/{class_id}/enroll_student",
                json={"student_id": student_id},
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao matricular aluno: {str(e)}"}

    def remove_student_from_class(self, class_id: str, student_id: str) -> Dict[str, Any]:
        """
        Remove um aluno de uma turma.
        POST /api/classes/<class_id>/remove_student
        """
        try:
            response = self.session.post(
                f"{self.base_url}/classes/{class_id}/remove_student",
                json={"student_id": student_id},
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao remover aluno: {str(e)}"}
    
    def get_all_students_by_teacher(self) -> Dict[str, Any]:
        """
        Busca TODOS os alunos de TODAS as turmas do professor logado.
        GET /api/teachers/all_students
        """
        try:
            response = self.session.get(
                f"{self.base_url}/teachers/all_students",
                headers=self._get_headers(),
                timeout=10
            )
            return self._handle_response(response)
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar alunos: {str(e)}"}
    
    # ==================== STATUS ====================
    
    def check_health(self) -> bool:
        """
        Verifica se a API está online
        
        Returns:
            bool: True se API está funcionando
        """
        try:
            response = self.session.get(
                f"{self.base_url}/status",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False


# Instância global do cliente
api_client = APIClient()


