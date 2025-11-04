import Artiste from '../../model/artiste.js';
import Extrait from '../../model/extrait.js';
import Interview from '../../model/interview.js';
import Nation from '../../model/nation.js';
import Question from '../../model/question.js';
import StyleMusical from '../../model/style_musical.js';
import Tag from '../../model/tag.js';
import Theme from '../../model/theme.js';

export class mmRoot {
}

export const LegendColorMap = {
    [mmRoot]: "#fff",
    [Artiste]: "#A0522D",
    [Extrait]: "#941C1C",
    [Interview]: "#9747FF",
    [Nation]: "#c24e00ff",
    [Question]: "#FFCD06",
    [StyleMusical]: "#010582",
    [Tag]: "#02b360ff",
    [Theme]: "#016969ff",
};

export const categorys = [
    Artiste,
    Extrait,
    Interview,
    Nation,
    StyleMusical,
    Tag,
    Theme,
]

export class mmLinkage {
    startnode;
    endnode;
    thickness;

    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    get length() {
        return Math.sqrt(Math.pow(this.endnode.x - this.startnode.x, 2) + Math.pow(this.endnode.y - this.startnode.y, 2));
    }

    get angle() {
        return Math.atan2(this.endnode.y - this.startnode.y, this.endnode.x - this.startnode.x) * 180 / Math.PI;
    }

    get style() {
        return {
            height: this.thickness + 'px',
            width: this.length + 'px',
            left: this.startnode.x + 'px',
            top: this.startnode.y + 'px',
            transform: `rotate(${this.angle}deg)`,
        };
    }
}

export class mmNode {
    x;
    y;
    depth;
    parent;
    category;
    uuid;
    constructor(x, y, depth, parent, category, uuid) {
        this.x = x;
        this.y = y;
        this.depth = depth;
        this.parent = parent;
        this.category = category;
        this.uuid = uuid;
    }

    getStyle(scale = 1.0, baseOffsetX = 0, baseOffsetY = 0) {
        const size = 100 * scale; // Base size 100px multiplied by scale

        return {
            'background-color': LegendColorMap[this.category] || '#000000',
            'left': (this.x + baseOffsetX) + 'px',
            'top': (this.y + baseOffsetY) + 'px',
            'width': size + 'px',
            'height': size + 'px',
            'font-size': (16 * scale) + 'px',
            'line-height': size + 'px',
        };
    }
}

export function mmget(vm) {
    // Clear existing nodes and linkages
    vm.nodes = [];
    vm.linkages = [];
    
    // Always start with root node
    let root = new mmNode(0, 0, 0, null, mmRoot, null);
    vm.nodes.push(root);
    
    // If there's a search term, add Question node
    if (vm.searchValue && vm.searchValue.trim() !== '') {
        let questionNode = new mmNode(0, 0, 1, root, Question, null);
        vm.nodes.push(questionNode);
        vm.linkages.push(new mmLinkage(root, questionNode, 1));
        
        // For now, just add some example nodes for search results
        // In a real implementation, you would search across all categories
        addChildNodes(vm, questionNode, 2);
    } else {
        // No search term - show all main categories
        addChildNodes(vm, root, 1);
    }
    
    // Position nodes after adding them
    positionNodes(vm);
}

function addChildNodes(vm, parentNode, depth) {
    const categoriesToShow = categorys.filter(cat => {
        // Filter out categories that are already in the chemin
        return !vm.chemin.some(chem => chem.category === cat);
    });
    
    categoriesToShow.forEach((category, index) => {
        // Temporary position - will be recalculated in positionNodes
        let childNode = new mmNode(0, 0, depth, parentNode, category, null);
        vm.nodes.push(childNode);
        vm.linkages.push(new mmLinkage(parentNode, childNode, 1));
    });
}

function positionNodes(vm) {
    // Position root at center
    const root = vm.nodes[0];
    root.x = 0;
    root.y = 0;
    
    // Get direct children of root
    const rootChildren = getDirectChildren(vm, root);
    
    if (rootChildren.length > 0) {
        const radius = 200; // Base radius from root
        const angleStep = (2 * Math.PI) / rootChildren.length;
        
        rootChildren.forEach((child, index) => {
            const angle = index * angleStep;
            child.x = root.x + radius * Math.cos(angle);
            child.y = root.y + radius * Math.sin(angle);
        });
        
        // Position grandchildren if they exist
        rootChildren.forEach(child => {
            const grandchildren = getDirectChildren(vm, child);
            if (grandchildren.length > 0) {
                positionChildrenInArc(vm, child, grandchildren, 150);
            }
        });
    }
}

function getDirectChildren(vm, parentNode) {
    return vm.nodes.filter(node => 
        vm.linkages.some(link => 
            link.startnode === parentNode && link.endnode === node
        )
    );
}

function positionChildrenInArc(vm, parent, children, radius) {
    if (children.length === 0) return;
    
    const angleStep = (2 * Math.PI) / children.length;
    
    // Calculate the direction from parent's parent to parent (for arc orientation)
    let referenceAngle = 0;
    if (parent.parent) {
        referenceAngle = Math.atan2(parent.y - parent.parent.y, parent.x - parent.parent.x);
    }
    
    children.forEach((child, index) => {
        const angle = referenceAngle + (index - (children.length - 1) / 2) * angleStep;
        child.x = parent.x + radius * Math.cos(angle);
        child.y = parent.y + radius * Math.sin(angle);
    });
}

export function mmsearch(obj, searchterm) {
    if (this.nodes[1]?.category.name != "question") {
        this.nodes.splice(1, 0, new mmNode(0, 0, 1, this.nodes[0], Question, null));
        linkages.push(new mmLinkage(nodelist[0], nodelist[1], 1));
    }
}