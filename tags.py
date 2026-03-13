import json
import os


class TagManager:
    
    def __init__(self, tags_file="tags.json"):
        self.tags_file = tags_file
        self.task_tags = {}
        self.load_tags()
    
    def load_tags(self):
        if os.path.exists(self.tags_file):
            try:
                with open(self.tags_file, 'r') as f:
                    self.task_tags = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.task_tags = {}
        else:
            self.task_tags = {}
    
    def save_tags(self):
        with open(self.tags_file, 'w') as f:
            json.dump(self.task_tags, f, indent=2)
    
    def add_tag_to_task(self, task_id, tag):
        if task_id not in self.task_tags:
            self.task_tags[task_id] = []
        
        tag = tag.lower().strip()
        if tag and tag not in self.task_tags[task_id]:
            self.task_tags[task_id].append(tag)
            self.save_tags()
            return True
        return False
    
    def remove_tag_from_task(self, task_id, tag):
        if task_id in self.task_tags:
            tag = tag.lower().strip()
            if tag in self.task_tags[task_id]:
                self.task_tags[task_id].remove(tag)
                self.save_tags()
                return True
        return False
    
    def get_tags_for_task(self, task_id):
        return self.task_tags.get(task_id, [])
    
    def get_tasks_by_tag(self, tag):
        tag = tag.lower().strip()
        return [task_id for task_id, tags in self.task_tags.items() if tag in tags]
    
    def get_all_tags(self):
        all_tags = set()
        for tags in self.task_tags.values():
            all_tags.update(tags)
        return sorted(list(all_tags))
    
    def delete_task_tags(self, task_id):
        if task_id in self.task_tags:
            del self.task_tags[task_id]
            self.save_tags()
            return True
        return False
    
    def get_tag_statistics(self):
        tag_counts = {}
        for tags in self.task_tags.values():
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts
