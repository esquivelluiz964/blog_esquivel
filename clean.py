import os
import shutil

def clean_project(root='.'):
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for dirname in dirnames:
            if dirname == '__pycache__':
                full_path = os.path.join(dirpath, dirname)
                shutil.rmtree(full_path, ignore_errors=True)
                print(f'Removido: {full_path}')
                removed += 1
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f'Removido: {file_path}')
                    removed += 1
                except Exception as e:
                    print(f'Erro ao remover {file_path}: {e}')
    print(f'\n🧹 Limpeza concluída! {removed} itens removidos.')

if __name__ == '__main__':
    clean_project()
