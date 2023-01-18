import datetime
from unittest.mock import mock_open, patch
import pytest
from writers import DataWriter 
from ingestors import DataIngestor

#Para evitar de ficar instaciando a mesma coisa em todas os metodos vamos utilizar a fixtures
# Temos que instaciar o patch do metodo abstrato 
@pytest.fixture
@patch("ingestors.DataIngestor.__abstractmethods__", set()) 
def data_ingestor_fixture():
    return DataIngestor(
            writer=DataWriter,
            coins=["TEST", "HOW"],
            defaultstartdate=datetime.date(2023,1,11)
        )

# Sobreescrever um metodo de uma determinada classe. Porque a classe que estamos testando é abstrata
# Vamos sobrescrever e tirar o medoto abstrato definido
@patch("ingestors.DataIngestor.__abstractmethods__", set()) 
class TestIngestor:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected
        
        
    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        excepted =  datetime.date(2023,1,11)
        assert actual == excepted
    
    # No ingestors.py esse comando cria um arquivo de checkpoint
    # Nesse teste não queremos que ele abra, vamos utilizar mock para testar
    #Vamos utilizar o patch novamente, vamos sobrescrever o metodo open do load_checkpoint
    # Utilizando "builtins.open" --- new_callable Vai ser uma nova forma de chamar o metodo
    # para sobrescrever o read que é chamado no metodo load_checkpoint
    #toda vez que utilizamos um mock, precisamos declarar ele nos argumentos da função, mesmo sem usar
    @patch("builtins.open", new_callable=mock_open, read_data="2023-1-12")
    def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        excepted =  datetime.date(2023, 1, 12)
        assert actual == excepted
        
    # Teste para ver se o checkpoint foi sobrescrito depois de rodar
    # Vamos criar um patch para o metodo update_checkpoint não rodar o self._write_checkpoint e criar um arquivo
    # Ele irá sobrescrever o write e retornar None
    @patch("ingestors.DataIngestor._write_checkpoint", return_value = None)
    def test_update_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor_fixture._update_checkpoint(value = datetime.date(2019, 1, 1))
        excepted = datetime.date(2019, 1, 1)
        actual = data_ingestor_fixture._checkpoint
        assert actual == excepted
        
        
    #Testar se o write está funcionando
    @patch("ingestors.DataIngestor._write_checkpoint", return_value = None)
    def test_update_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor_fixture._update_checkpoint(value = datetime.date(2019, 1, 1))
        #Comando para verificar se o mock foi chamado
        mock.assert_called_once()
        
    # Write é a função que cria o arquivo, não queremos criar no teste
    # Vamos utilizar o mock para sobrescrever e não precisar criar quando ele rodar 
    # Quando eu tenho dois patch, sempre o patch mais acima vai ser o ultimo a declarar no metodo
    @patch("builtins.open", new_callable=mock_open, read_data="2023-1-12")
    @patch("ingestors.DataIngestor._checkpoint_filename", return_value ="foobar.checkpoint")
    def test_write_checkpoint(self, mock_checkpoint_filename ,mock_open_file, data_ingestor_fixture):
        data_ingestor_fixture._write_checkpoint()
        # Verificar que ele foi chamado com o checkpoint_filename no modo W
        mock_open_file.assert_called_with(mock_checkpoint_filename, "w")
          
        
        
        